from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from .api import BSDModel
# from .auth import Constituent - no circular imports
import datetime, localflavor.us.models


# should be a setting, but for quick and dirty purposes..
OUR_REVOLUTION_CHAPTER_ID = 2


# looking for this? check auth.py, it got involved.
# class Constituent(BSDModel):
#     pass


class OurRevolutionObjectManager(models.Manager):

    def get_queryset(self):
        return super(OurRevolutionObjectManager, self).get_queryset().filter(chapter_id=OUR_REVOLUTION_CHAPTER_ID)


class ConstituentEmail(models.Model):
    cons_email_id = models.AutoField(primary_key=True)
    cons = models.ForeignKey('Constituent', related_name="emails")
    cons_email_type_id = models.IntegerField()  # todo - look into this better.
    is_primary = models.IntegerField()
    email = models.CharField(max_length=128)
    canonical_local_part = models.CharField(max_length=128, blank=True, null=True)
    domain = models.CharField(max_length=128, blank=True, null=True)
    double_validation = models.CharField(max_length=32, blank=True, null=True)
    create_dt = models.DateTimeField(blank=True, null=True)
    create_app = models.CharField(max_length=128, blank=True, null=True)
    create_user = models.CharField(max_length=128, blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    modified_app = models.CharField(max_length=128, blank=True, null=True)
    modified_user = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cons_email'


class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state_cd = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=16, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    create_dt = models.DateTimeField(blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    create_admin_user = models.ForeignKey('Constituent', blank=True, null=True)
    status = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chapter'


class ConstituentChapter(models.Model):
    cons = models.ForeignKey('Constituent')
    chapter = models.ForeignKey(Chapter)

    class Meta:
        managed = False
        db_table = 'cons__chapter'
        unique_together = (('cons', 'chapter'),)



class EventType(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    contribution_page_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    van_campaign_title = models.CharField(max_length=128, blank=True, null=True)
    detail_label = models.CharField(max_length=128, blank=True, null=True)
    detail_text = models.TextField(blank=True, null=True)
    can_users_create = models.IntegerField()
    fixed_title = models.CharField(max_length=128, blank=True, null=True)
    fixed_day = models.DateField(blank=True, null=True)
    fixed_tz = models.CharField(max_length=40, blank=True, null=True)
    fixed_time = models.TimeField(blank=True, null=True)
    is_searchable = models.IntegerField()
    host_mailing_addr = models.IntegerField()
    contact_phone = models.IntegerField()
    can_set_capacity = models.IntegerField()
    expir_dt = models.DateTimeField(blank=True, null=True)
    pledge_show = models.IntegerField()
    pledge_source = models.CharField(max_length=128, blank=True, null=True)
    pledge_subsource = models.CharField(max_length=128, blank=True, null=True)
    pledge_require = models.IntegerField()
    pledge_min = models.FloatField(blank=True, null=True)
    pledge_max = models.FloatField(blank=True, null=True)
    pledge_suggest = models.FloatField(blank=True, null=True)
    shifts_allow = models.IntegerField(blank=True, null=True)
    multiple_dates_allow = models.IntegerField(blank=True, null=True)
    rsvp_allow = models.IntegerField(blank=True, null=True)
    rsvp_allow_reminder_email = models.IntegerField()
    rsvp_require_signup = models.IntegerField(blank=True, null=True)
    rsvp_disallow_account = models.IntegerField(blank=True, null=True)
    rsvp_request_first_last_name = models.IntegerField(blank=True, null=True)
    rsvp_require_first_last_name = models.IntegerField(blank=True, null=True)
    rsvp_use_default_email_message = models.IntegerField(blank=True, null=True)
    rsvp_collect_employer_occupation = models.IntegerField(blank=True, null=True)
    rsvp_require_employer_occupation = models.IntegerField(blank=True, null=True)
    rsvp_allow_host_override_email_message = models.IntegerField(blank=True, null=True)
    rsvp_send_confirmation_email = models.IntegerField(blank=True, null=True)
    rsvp_reason = models.TextField(blank=True, null=True)
    rsvp_email_message = models.TextField(blank=True, null=True)
    rsvp_email_message_html = models.TextField(blank=True, null=True)
    rsvp_redirect_url = models.CharField(max_length=255)
    attendee_volunteer_show = models.IntegerField()
    attendee_volunteer_message = models.TextField()
    approval_require = models.IntegerField()
    map_marker_storage_key = models.CharField(max_length=32, blank=True, null=True)
    map_marker_width = models.IntegerField(blank=True, null=True)
    map_marker_height = models.IntegerField(blank=True, null=True)
    chapter = models.ForeignKey(Chapter)
    facebook_default_message = models.TextField()
    twitter_default_message = models.CharField(max_length=140)
    van_event_type_name = models.CharField(max_length=255, blank=True, null=True)
    van_program_type_name = models.CharField(max_length=255, blank=True, null=True)
    sync_to_van = models.IntegerField()
    create_dt = models.DateTimeField(blank=True, null=True)
    create_app = models.CharField(max_length=128, blank=True, null=True)
    create_user = models.CharField(max_length=128, blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    modified_app = models.CharField(max_length=128, blank=True, null=True)
    modified_user = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)
    enable_addr_autofill = models.IntegerField()
    enable_host_addr_autofill = models.IntegerField()
    objects = OurRevolutionObjectManager()
    
    def __unicode__(self):
        return self.name
    

    class Meta:
        managed = False
        db_table = 'event_type'




class Event(BSDModel):
    FORBIDDEN_FIELDS = ["event_id", "latitude", "longitude", # 'start_day',
                        "host_addr_addressee", "host_addr_addr1", "host_addr_addr2",
                        "host_addr_zip", "host_addr_city", "host_addr_state_cd",
                        "host_addr_country"]
                        
    VISIBILITY_CHOICES = (
        (0, 'NONE'),
        (1, 'COUNT'),
        (2, 'FIRST'),
    )
    TIME_ZONE_CHOICES = (('America/%s' % pair[1], pair[0]) for pair in (('Eastern', 'New_York'), ('Central', 'Chicago'), ('Mountain', 'Denver'), ('Pacific', 'Los_Angeles'), ('Alaska', 'Anchorage'), ('Hawaii', 'Adak')))
    DURATION_MULTIPLIER = (
        (1, 'Minutes'),
        (60, 'Hours'),
    )
    event_id = models.AutoField(primary_key=True)
    event_id_obfuscated = models.CharField(max_length=16, blank=True, null=True)
    event_type = models.ForeignKey(EventType, verbose_name="Choose an Event Type")
    creator_cons = models.ForeignKey('Constituent')
    contribution_page_id = models.IntegerField(blank=True, null=True)
    outreach_page_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    creator_name = models.CharField(max_length=255, verbose_name='Host Name')
    start_day = models.DateField(verbose_name='Date')
    start_time = models.TimeField(verbose_name='Start Time')
    start_dt = models.DateTimeField()
    start_tz = models.CharField(max_length=40, blank=False, null=True, verbose_name='Time Zone', choices=TIME_ZONE_CHOICES, default='America/Eastern')
    duration = models.IntegerField()
    parent_event_id = models.IntegerField(default=0)
    venue_name = models.CharField(max_length=255, verbose_name='Venue Name')
    venue_addr1 = models.CharField(max_length=255, verbose_name='Venue Address')
    venue_addr2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Venue Address #2')
    venue_city = models.CharField(max_length=64, verbose_name='Venue City')
    # venue_state_cd = models.CharField(max_length=100, verbose_name='Venue State')
    venue_state_cd = localflavor.us.models.USStateField(verbose_name='Venue State')
    venue_zip = models.CharField(max_length=16, verbose_name='Venue Zip Code')
    venue_country = models.CharField(max_length=2, verbose_name='Venue Country', default='US')
    venue_directions = models.TextField(blank=True, null=True, verbose_name='Directions to Venue')
    latitude = models.FloatField()
    longitude = models.FloatField()
    host_addr_addressee = models.CharField(max_length=255, blank=True, null=True)
    host_addr_addr1 = models.CharField(max_length=255, blank=True, null=True)
    host_addr_addr2 = models.CharField(max_length=255, blank=True, null=True)
    host_addr_zip = models.CharField(max_length=16, blank=True, null=True)
    host_addr_city = models.CharField(max_length=64, blank=True, null=True)
    host_addr_state_cd = models.CharField(max_length=100, blank=True, null=True)
    host_addr_country = models.CharField(max_length=2)
    host_receive_rsvp_emails = models.IntegerField(default=1, verbose_name='Notify me when new people RSVP')
    contact_phone = models.CharField(max_length=25)
    public_phone = models.IntegerField(default=1, verbose_name='Make my phone number public to attendees')
    capacity = models.IntegerField(verbose_name='Capacity Limit', help_text="Including guests. Leave 0 for unlimited.", default=0)
    all_shifts_full = models.IntegerField(default=0)
    closed_msg = models.TextField(blank=True, null=True)
    attendee_visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default=1)
    attendee_require_phone = models.IntegerField(default=0)
    attendee_volunteer_show = models.IntegerField(default=0)
    attendee_volunteer_message = models.TextField(default=0)
    is_official = models.IntegerField(blank=True, null=True)
    pledge_override_type = models.IntegerField(default=0)
    pledge_show = models.IntegerField(default=0)
    pledge_source = models.CharField(max_length=128, blank=True, null=True)
    pledge_subsource = models.CharField(max_length=128, blank=True, null=True)
    pledge_require = models.IntegerField(default=0)
    pledge_min = models.FloatField(blank=True, null=True)
    pledge_max = models.FloatField(blank=True, null=True)
    pledge_suggest = models.FloatField(blank=True, null=True)
    rsvp_use_default_email_message = models.IntegerField(blank=True, null=True, default=1)
    rsvp_email_message = models.TextField(blank=True, null=True)
    rsvp_email_message_html = models.TextField(blank=True, null=True)
    rsvp_use_reminder_email = models.IntegerField()
    rsvp_reminder_email_sent = models.IntegerField()
    rsvp_email_reminder_hours = models.IntegerField(blank=True, null=True)
    rsvp_allow = models.IntegerField(blank=True, null=True)
    rsvp_require_signup = models.IntegerField(blank=True, null=True)
    rsvp_disallow_account = models.IntegerField(blank=True, null=True)
    rsvp_reason = models.TextField(blank=True, null=True)
    rsvp_redirect_url = models.CharField(max_length=255, null=True, blank=True, default='')
    is_searchable = models.IntegerField(default=1)
    flag_approval = models.IntegerField(default=0)
    chapter = models.ForeignKey(Chapter)
    create_dt = models.DateTimeField(blank=True, null=True)
    create_app = models.CharField(max_length=128, blank=True, null=True)
    create_user = models.CharField(max_length=128, blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    modified_app = models.CharField(max_length=128, blank=True, null=True)
    modified_user = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField(default=1)
    note = models.CharField(max_length=255, blank=True, null=True)
    objects = OurRevolutionObjectManager()
    
    def __unicode__(self):
        return self.name
    
    def bsd_error_handle(self, error_dict):
        print error_dict
        errors = {}
        print error_dict
        for field, error_list in error_dict.iteritems():
            human_friendly_label = self._meta.get_field(field).verbose_name.title()
            if 'required' in error_list:
                errors[field] = ValidationError("%s is required, please check your input and try again." % human_friendly_label)
            elif 'regex' in error_list or 'string' in error_list:
                errors[field] = ValidationError("Please check your input on %s." % human_friendly_label)
            else:
                errors[field] = ValidationError("Please check your input on %s." % human_friendly_label)
        raise ValidationError(errors)

        
    def get_absolute_url(self):
        return "https://go.ourrevolution.com/page/event/detail/canvassforourrevolution/%s" % self.event_id_obfuscated
    
    def get_api_data(self):
        return self._scrub_event_data_for_api(super(Event, self).get_api_data())
        
        
    def _scrub_event_data_for_api(self, data):
        
        # needs integers for boolean representations
        for field in ['rsvp_use_reminder_email', 'rsvp_reminder_email_sent']:
            data[field] = int(bool(data[field]))
            
        # stored as an integer, but needs that string label for the API            
        data['attendee_visibility'] = self.VISIBILITY_CHOICES[int(data.get('attendee_visiblity', 2))][1]

        # days is just its own weird mess
        data['days'] = [{'start_datetime_system': datetime.datetime.combine(data['start_day'], data['start_time']),
                    'duration': data['duration']}]

        del data['start_day']
        
        return data
    

    def get_api_endpoint(self):
        path = "create_event"
        if self.pk:
            path = "update_event"
        return "/event/%s" % path


    class Meta:
        managed = False
        db_table = 'event'


class EventAttendee(models.Model):
    event_attendee_id = models.AutoField(primary_key=True)
    attendee_cons_id = models.IntegerField()
    event_id = models.IntegerField()
    will_attend = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    guests = models.IntegerField(blank=True, null=True)
    pledge_amt = models.IntegerField(blank=True, null=True)
    pledge_method = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    is_potential_volunteer = models.IntegerField()
    is_reminder_sent = models.IntegerField()
    addr1 = models.CharField(max_length=255, blank=True, null=True)
    addr2 = models.CharField(max_length=255, blank=True, null=True)
    addr3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state_cd = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=16, blank=True, null=True)
    zip_4 = models.CharField(max_length=4, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    create_dt = models.DateTimeField(blank=True, null=True)
    create_app = models.CharField(max_length=128, blank=True, null=True)
    create_user = models.CharField(max_length=128, blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    modified_app = models.CharField(max_length=128, blank=True, null=True)
    modified_user = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_attendee'


class ConstituentAddress(models.Model):
    cons_addr_id = models.AutoField(primary_key=True)
    cons = models.ForeignKey('Constituent', related_name="addresses")
    cons_addr_type_id = models.IntegerField()   # todo -- look into further.
    is_primary = models.IntegerField()
    addr1 = models.CharField(max_length=255, blank=True, null=True)
    addr2 = models.CharField(max_length=255, blank=True, null=True)
    addr3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state_cd = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=16, blank=True, null=True)
    zip_4 = models.CharField(max_length=4, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    addr_aug_ver = models.IntegerField()
    addr_aug_dt = models.DateTimeField(blank=True, null=True)
    geocoder_accuracy = models.IntegerField(blank=True, null=True)
    create_dt = models.DateTimeField(blank=True, null=True)
    create_app = models.CharField(max_length=128, blank=True, null=True)
    create_user = models.CharField(max_length=128, blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    modified_app = models.CharField(max_length=128, blank=True, null=True)
    modified_user = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cons_addr'
        
        
        
class ConsEmailChapterSubscription(models.Model):
    cons_email_chapter_subscription_id = models.AutoField(primary_key=True)
    cons_email = models.ForeignKey('ConstituentEmail')
    cons = models.ForeignKey('Constituent')
    chapter = models.ForeignKey('Chapter')
    isunsub = models.IntegerField()
    unsub_dt = models.DateTimeField(blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cons_email_chapter_subscription'
        unique_together = (('cons_email', 'chapter'),)