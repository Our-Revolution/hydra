from __future__ import unicode_literals
from django.db import models


class Slack(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField()
    subdomain = models.CharField(max_length=1024)
    api_key = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.name