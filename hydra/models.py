from django.db import models
from bsd.auth import Constituent
from bsd.models import Event


class EventPromotionRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('approved', 'Approved'),
        ('sent', 'Sent')
    )
    subject = models.CharField(max_length=128)
    message = models.CharField(max_length=1024)
    volunteer_count = models.IntegerField()
    event = models.ForeignKey(Event)
    host = models.ForeignKey(Constituent)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default='new')
    recipients = models.ManyToManyField(Constituent, blank=True, related_name='event_promotions')
