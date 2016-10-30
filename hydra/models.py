from django.db import models
from bsd.auth import Constituent
from bsd.models import Event

from .fields import CrossDatabaseForeignKey


class EventPromotionRequestThrough(models.Model):
    event_promotion_request = models.ForeignKey('EventPromotionRequest')
    recipient = CrossDatabaseForeignKey(Constituent, db_constraint=False)



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
            
            
        # todos:
        
        # convert event location to point
        
        # find ?? 5 ?? zip codes nearby; step up from there



        # find constituents, by cons_addr --> zip code
        
        # exclude folks who have received one in the last ?? 14 ?? days
        
        # exclude folks who have unsubscribed
        
        # mail via mailgun.
            
        self.sent = datetime.datetime.now()
        self.save()
    

    def save(self, *args, **kwargs):
        if not self.host_id and self.event and self.event.creator_cons:
            self.host = self.event.creator_cons
        return super(EventPromotionRequest, self).save(*args, **kwargs)
        if not self.sent and self.status == 'sent':
            self._send()
        