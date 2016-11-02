from django.conf import settings
from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as geo_models 
from django.contrib.gis.measure import Distance
from itertools import chain
from localflavor.us.models import USZipCodeField
import datetime, requests

from bsd.auth import Constituent
from bsd.models import ConstituentAddress, Event
from .fields import CrossDatabaseForeignKey


import logging


logger = logging.getLogger(__name__)


class EventPromotionRequestThrough(models.Model):
    event_promotion_request = models.ForeignKey('EventPromotionRequest')
    recipient = CrossDatabaseForeignKey(Constituent, db_constraint=False, related_name='+')



class EventPromotionRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('approved', 'Approved'),
        ('sent', 'Sent')
    )
    sender_display_name = models.CharField(max_length=128, null=True)
    sender_email = models.EmailField(null=True)
    subject = models.CharField(max_length=128)
    message = models.CharField(max_length=1024)
    volunteer_count = models.IntegerField()
    event = CrossDatabaseForeignKey(Event, db_constraint=False)
    host = CrossDatabaseForeignKey(Constituent, db_constraint=False, related_name="event_promotion_requests")
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default='new')
    submitted = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    sent = models.DateTimeField(null=True, blank=True)
    recipients = models.ManyToManyField(Constituent, through="EventPromotionRequestThrough", related_name="event_promotions")
    
    
    def _send(self, preview=None):

        # todo - this preview + sending is getting unwieldy -- need a mini refactor.
        
        if not preview:

            if self.sent:
                # todo: raise something; only send once.
                return None
            
            # convert event location to point
            point = Point(x=self.event.longitude, y=self.event.latitude, srid=4326)
            
            constituent_ids_to_email = []
            
            logger.debug("excluding ...")
            
            # anything > 2 weeks ago, do not email.
            constituents_to_exclude = list(EventPromotionRequestThrough.objects.filter(event_promotion_request__sent__gt=datetime.datetime.now() - datetime.timedelta(days=14)).values_list('recipient_id', flat=True))
            
            for zip_distance in [1, 2, 5, 8, 10, 25, 50]:
            
                logger.debug("Finding zips within %s miles ..." % zip_distance)
            
                for zip in ZipCode.objects.filter(centroid__distance_lte=(point, Distance(mi=zip_distance))):
                
                    logger.debug("Found %s" % zip.zip)

                    candidate_constituents = Constituent.objects.filter(addresses__zip=zip.zip) \
                                    .filter(emails__isnull=False) \
                                    .exclude(pk__in=constituents_to_exclude) \
                                    .exclude(consemailchaptersubscription__isunsub=1) \
                                    .distinct() \
                                    .values_list('pk', flat=True)
                                    
                    logger.debug("Found %s addresses... " % len(candidate_constituents))
                    
                    # add as many as we need.
                    constituent_ids_to_email += list(candidate_constituents[0:min(self.volunteer_count if len(constituent_ids_to_email) == 0 else len(constituent_ids_to_email), self.volunteer_count - len(constituent_ids_to_email))])
                    
                    if len(constituent_ids_to_email) >= self.volunteer_count:
                        break
                        
                if len(constituent_ids_to_email) >= self.volunteer_count:
                    break
                    
            logger.debug("All done, we found enough.")
            
            constituents = Constituent.objects.filter(pk__in=constituent_ids_to_email)
            
            email_addresses = constituents.order_by('-emails__is_primary').values_list('emails__email', flat=True)

        else:
            email_addresses = [e.strip() for e in preview.split(',')]
        
        logger.debug("MAILING !!!")
        
        logger.debug(self.subject)
        logger.debug(self.message)
        logger.debug(email_addresses)
        
        # debug measure.        
        requests.post("https://api.mailgun.net/v3/%s/messages" % settings.MAILGUN_SERVER_NAME,
                        auth=("api", settings.MAILGUN_ACCESS_KEY),
                        data={"from": "%s <%s>" % (self.sender_display_name, self.sender_email),
                                  "to": [", ".join(email_addresses)],
                                  "subject": self.subject,
                                  "text": self.message})

        if not preview:

            logger.debug("OK time to add recipients for book keeping ...")
                                      
            # add as recipients for log keeping
            EventPromotionRequestThrough.objects.bulk_create([
                EventPromotionRequestThrough(event_promotion_request_id=self.pk, recipient_id=recipient) for recipient in constituents.values_list('pk', flat=True)
            ])
                
            self.sent = datetime.datetime.now()
            self.save()
    

    def save(self, *args, **kwargs):
        logger.debug('saving')
        
        if not self.host_id and self.event and self.event.creator_cons:
            self.host = self.event.creator_cons

        preview = kwargs.pop('preview', False)

        super(EventPromotionRequest, self).save(*args, **kwargs)
        
        if preview:
            self._send(preview=preview)

        elif not self.sent and self.status == 'sent':
            self._send()
        
        return self
            
            

class ZipCode(models.Model):
    zip = USZipCodeField()
    centroid = geo_models.PointField(srid=4326, null=True, blank=True)
    geom = geo_models.MultiPolygonField(srid=4326)