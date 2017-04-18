from __future__ import unicode_literals

from django.db import models


class Group(models.Model):    
    name = models.CharField(max_length=64, null=True, blank=False, verbose_name="Group Name")
    slug = models.SlugField(null=True, blank=False, unique=True, max_length=100)
    signup_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    group_id = models.CharField(max_length=4,null=True, blank=False, unique=True)
    
    rep_email = models.EmailField(null=True, blank=False, verbose_name="Contact Email", max_length=254)
    rep_first_name = models.CharField(max_length=35, null=True, blank=False, verbose_name="First Name")
    rep_last_name = models.CharField(max_length=35, null=True, blank=False, verbose_name="Last Name")
    rep_postal_code = models.CharField(max_length=12, null=True, blank=True, verbose_name="Postal Code")
    
    county = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    postal_code = models.CharField(max_length=12, null=True, blank=True, verbose_name="Postal Code")
        
    size = models.CharField(max_length=21, null=True, blank=True, verbose_name="Group Size")
    
    last_meeting = models.DateTimeField(null=True, blank=True, verbose_name="Date of Last Meeting")
    
    meeting_address_line1 = models.CharField("Address Line 1", max_length = 45, null=True, blank=True)
    meeting_address_line2 = models.CharField("Address Line 2", max_length = 45, null=True, blank=True)
    meeting_postal_code = models.CharField("Postal Code", max_length = 12, null=True, blank=True)
    meeting_city = models.CharField(max_length = 64, null=True, blank=True, verbose_name="City")
    meeting_state_province = models.CharField("State/Province", max_length = 40, null=True, blank=True)
    
    TYPES_OF_ORGANIZING_CHOICES = (
        ('direct-action', 'Direct Action'),
        ('electoral', 'Electoral Organizing'),
        ('legistlative', 'Advocating for Legislation or Ballot Measures'),
        ('community', 'Community Organizing'),
        ('other', 'Other')
    )
    other_types_of_organizing = models.TextField(null=True, blank=True, verbose_name="Other Types of Organizing", max_length=250)
    
    description = models.TextField(null=True, blank=False, max_length=250, verbose_name="Description (250 characters or less)")
    other_issues = models.TextField(null=True, blank=True, max_length=250, verbose_name="Other Issues")
    
    constituency = models.TextField(null=True, blank=True, max_length=250)
    
    facebook_url = models.URLField(null=True, blank=True, verbose_name="Facebook URL", max_length=255)
    twitter_url = models.URLField(null=True, blank=True, verbose_name="Twitter URL", max_length=255)
    website_url = models.URLField(null=True, blank=True, verbose_name="Website URL", max_length=255)
    instagram_url = models.URLField(null=True, blank=True, verbose_name="Instagram URL", max_length=255)
    other_social = models.TextField(null=True, blank=True, verbose_name="Other Social Media", max_length=250)
    
    STATUSES = (
       ('submitted', 'Submitted'),
       ('signed-mou', 'Signed MOU'),
       ('approved', 'Approved'),
       ('removed', 'Removed') # can flesh out later
   ) 
    status = models.CharField(max_length=16, choices=STATUSES, default='submitted')
    # source = models.CharField(max_length=17, null=True, blank=True)
    # subsource = models.FloatField(null=True, blank=True)
    # i_p__address = models.CharField(max_length=16, null=True, blank=True)
    # constituent__id = models.IntegerField(null=True, blank=True)
    # signup__id = models.IntegerField(null=True, blank=True)
        
    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "local_groups_group"