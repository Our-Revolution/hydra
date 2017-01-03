from django.conf import settings
from django.core.mail import mail_admins
from django.db import models
from django.db.models import Count
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as geo_models 
from django.contrib.gis.measure import Distance
from itertools import chain
from localflavor.us.models import USZipCodeField
import datetime, json, requests

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
        ('sent', 'Sent'),
        ('skipped', 'Skipped')
    )
    sender_display_name = models.CharField(max_length=128, null=True)
    sender_email = models.EmailField(null=True)
    subject = models.CharField(max_length=128)
    message = models.CharField(max_length=2048)
    volunteer_count = models.IntegerField()
    event = CrossDatabaseForeignKey(Event, db_constraint=False)
    host = CrossDatabaseForeignKey(Constituent, db_constraint=False, related_name="event_promotion_requests")
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default='new')
    submitted = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    sent = models.DateTimeField(null=True, blank=True)
    recipients = models.ManyToManyField(Constituent, through="EventPromotionRequestThrough", related_name="event_promotions")

    @staticmethod
    def _send_approved_emails():

        reqs = EventPromotionRequest.objects.filter(status='approved', )

        for req in reqs:
            req._send()


    @staticmethod
    def _mark_approved_as_skipped():
        EventPromotionRequest.objects.filter(status='approved').update(status='skipped')

    def _do_send_to_recipients(self, email_addresses):

        recipient_variables = dict((email, {}) for email in email_addresses)
        
        post = requests.post("https://api.mailgun.net/v3/%s/messages" % settings.MAILGUN_SERVER_NAME,
                        auth=("api", settings.MAILGUN_ACCESS_KEY),
                        data={"from": "%s <%s>" % (self.sender_display_name, self.sender_email),
                                  "to": [", ".join(email_addresses)],
                                  "subject": self.subject,
                                  "text": self.message,
                                  "recipient-variables": (json.dumps(recipient_variables))
                            })

        if post.status_code != 200:
            message = """
Error message: %(error_message)s

Event link: %(event_link)s

Promotion link: %(promotion_link)s""" % {
                                            'error_message': json.loads(post.text)['message'],\
                                            'event_link': self.event.get_absolute_url(),
                                            'promotion_link': "http://events.ourrevolution.com/admin/hydra/eventpromotionrequest/%s/change/" % self.pk
                                        }
            mail_admins("Error sending promotion email", message, fail_silently=True)

        return post
    
    
    def _send(self):

        if self.sent or self.status == 'sent':
            # todo: raise something; only send once.
            return None
        
        # convert event location to point
        point = Point(x=self.event.longitude, y=self.event.latitude, srid=4326)
        
        constituent_ids_to_email = []

        zips_tried = []
        
        logger.debug("excluding ...")
        
        # anything > 2 weeks ago, do not email.
        constituents_to_exclude = list(EventPromotionRequestThrough.objects.filter(event_promotion_request__sent__gt=datetime.datetime.now() - datetime.timedelta(days=14)).annotate(req_last_two_weeks=Count('event_promotion_request')).filter(req_last_two_weeks__gt=2).values_list('recipient_id', flat=True))
        
        for zip_distance in [1, 2, 5, 8, 10, 15]:
        
            logger.debug("Finding zips within %s miles ..." % zip_distance)
        
            for zipcode in ZipCode.objects.filter(centroid__distance_lte=(point, Distance(mi=zip_distance))).exclude(zip__in=zips_tried):

                zips_tried.append(zipcode.zip)
            
                logger.debug("Found %s" % zipcode.zip)

                candidate_constituents = Constituent.objects.filter(addresses__zip=zipcode.zip) \
                                .filter(emails__isnull=False) \
                                .filter(sendableconsgroup__isnull=False) \
                                .exclude(pk__in=constituents_to_exclude) \
                                .exclude(pk__in=constituent_ids_to_email) \
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
        
        email_addresses = constituents.filter(emails__is_primary=1).values_list('emails__email', flat=True)[0:self.volunteer_count]
        
        logger.debug("MAILING !!!")
        
        logger.debug(self.subject)
        logger.debug(self.message)
        logger.debug(email_addresses)

        # empty? keep moving.
        if email_addresses:

            post = self._do_send_to_recipients(email_addresses=email_addresses)

        logger.debug("OK time to add recipients for book keeping ...")
                                  
        # add as recipients for log keeping
        EventPromotionRequestThrough.objects.bulk_create([
            EventPromotionRequestThrough(event_promotion_request_id=self.pk, recipient_id=recipient) for recipient in constituents.values_list('pk', flat=True)
        ])
        
        self.status = 'sent'
        self.sent = datetime.datetime.now()
        self.save()
    

    def save(self, *args, **kwargs):
        logger.debug('saving')
        
        if not self.host_id and self.event and self.event.creator_cons:
            self.host = self.event.creator_cons

        preview = kwargs.pop('preview', False)

        super(EventPromotionRequest, self).save(*args, **kwargs)
        
        if preview:
            emails = [e.strip() for e in preview.split(',')]
            self._do_send_to_recipients(email_addresses=emails)
        
        return self
            
            

class ZipCode(models.Model):
    zip = USZipCodeField()
    centroid = geo_models.PointField(srid=4326, null=True, blank=True)
    geom = geo_models.MultiPolygonField(srid=4326)