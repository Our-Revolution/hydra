from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as geo_models 
from django.contrib.gis.measure import Distance
from itertools import chain
from localflavor.us.models import USZipCodeField
import datetime

from bsd.auth import Constituent
from bsd.models import ConstituentAddress, Event
from .fields import CrossDatabaseForeignKey


class EventPromotionRequestThrough(models.Model):
    event_promotion_request = models.ForeignKey('EventPromotionRequest')
    recipient = CrossDatabaseForeignKey(Constituent, db_constraint=False, related_name='+')



class EventPromotionRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('approved', 'Approved'),
        ('sent', 'Sent')
    )
    subject = models.CharField(max_length=128)
    message = models.CharField(max_length=1024)
    volunteer_count = models.IntegerField()
    event = CrossDatabaseForeignKey(Event, db_constraint=False)
    host = CrossDatabaseForeignKey(Constituent, db_constraint=False, related_name="event_promotion_requests")
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default='new')
    submitted = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    sent = models.DateTimeField(null=True, blank=True)
    recipients = models.ManyToManyField(Constituent, through="EventPromotionRequestThrough", related_name="event_promotions")
    
    
    def _send(self):
        if self.sent:
            # todo: raise something; only send once.
            return None
            
        # convert event location to point
        point = Point(x=self.event.longitude, y=self.event.latitude, srid=4326)
        
        constituents_to_email = []
        
        # anything > 2 weeks ago, do not email.
        constituents_to_exclude = list(EventPromotionRequestThrough.objects.filter(event_promotion_request__sent__gt=datetime.datetime.now() - datetime.timedelta(days=14)).values_list('recipient_id', flat=True))
        
        for zip_distance in [1, 2, 5, 8, 10, 25, 50]:
        
            for zip in ZipCode.objects.filter(centroid__distance_lte=(point, Distance(mi=zip_distance))):
                
                addresses = ConstituentAddress.objects.filter(zip=zip.zip) \
                                .filter(cons__constituentemail__isnull=False) \
                                .exclude(cons_id__in=constituents_to_exclude) \
                                .exclude(cons__consemailchaptersubscription__isunsub=1) \
                                .distinct() \
                                .order_by('-cons__constituentemail__is_primary') \
                                .values_list('cons__constituentemail__email', flat=True)
                                
                print addresses.count()
                import ipdb; ipdb.set_trace()
                
                # add as many as we need.
                constituents_to_email += list(addresses[0:min(self.volunteer_count if len(constituents_to_email) == 0 else len(constituents_to_email), self.volunteer_count - len(constituents_to_email))])
                
                if len(constituents_to_email) >= self.volunteer_count:
                    break
                    
            if len(constituents_to_email) >= self.volunteer_count:
                break
                
                
        import ipdb; ipdb.set_trace()
        
        # mail via mailgun.
            
        # self.sent = datetime.datetime.now()
        # self.save()
    

    def save(self, *args, **kwargs):
        if not self.host_id and self.event and self.event.creator_cons:
            self.host = self.event.creator_cons
        return super(EventPromotionRequest, self).save(*args, **kwargs)
        if not self.sent and self.status == 'sent':
            self._send()
            
            

class ZipCode(models.Model):
    zip = USZipCodeField()
    centroid = geo_models.PointField(srid=4326, null=True, blank=True)
    geom = geo_models.MultiPolygonField(srid=4326)