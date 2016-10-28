from __future__ import unicode_literals
from django.db import models
from .api import BSDModel


# should be a setting, but for quick and dirty purposes..
OUR_REVOLUTION_CHAPTER_ID = 2



class OurRevolutionObjectManager(models.Manager):

    def get_queryset(self):
        return super(OurRevolutionObjectManager, self).get_queryset().filter(chapter_id=OUR_REVOLUTION_CHAPTER_ID)



class Constituent(models.Model):
    cons_id = models.AutoField(primary_key=True)
    cons_source_id = models.IntegerField()
    prefix = models.CharField(max_length=16, blank=True, null=True)
    firstname = models.CharField(max_length=128, blank=True, null=True)
    middlename = models.CharField(max_length=128, blank=True, null=True)
    lastname = models.CharField(max_length=128, blank=True, null=True)
    suffix = models.CharField(max_length=16, blank=True, null=True)
    salutation = models.CharField(max_length=64, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    birth_dt = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    employer = models.CharField(max_length=128, blank=True, null=True)
    occupation = models.CharField(max_length=128, blank=True, null=True)
    income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    source = models.CharField(max_length=128, blank=True, null=True)
    subsource = models.CharField(max_length=128, blank=True, null=True)
    userid = models.CharField(max_length=128, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_validated = models.IntegerField()
    is_banned = models.IntegerField()
    change_password_next_login = models.IntegerField()
    create_dt = models.DateTimeField(blank=True, null=True)
    create_app = models.CharField(max_length=128, blank=True, null=True)
    create_user = models.CharField(max_length=128, blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    modified_app = models.CharField(max_length=128, blank=True, null=True)
    modified_user = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)

    class Meta:
        managed = False
        db_table = 'cons'


class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state_cd = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=16, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    create_dt = models.DateTimeField(blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    create_admin_user = models.ForeignKey(Constituent, blank=True, null=True)
    status = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chapter'


class ConstituentChapter(models.Model):
    cons = models.ForeignKey(Constituent)
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

    class Meta:
        managed = False
        db_table = 'event_type'




class Event(BSDModel):
    FORBIDDEN_FIELDS = ["event_id", "latitude", "longitude", "start_day", \
                        "host_addr_addressee", "host_addr_addr1", "host_addr_addr2", \
                        "host_addr_zip", "host_addr_city", "host_addr_state_cd", \
                        "host_addr_country"]
    event_id = models.AutoField(primary_key=True)
    event_id_obfuscated = models.CharField(max_length=16, blank=True, null=True)
    event_type_id = models.IntegerField()
    creator_cons = models.ForeignKey(Constituent)
    contribution_page_id = models.IntegerField(blank=True, null=True)
    outreach_page_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    creator_name = models.CharField(max_length=255, blank=True, null=True)
    start_day = models.DateField()
    start_time = models.TimeField()
    start_dt = models.DateTimeField()
    start_tz = models.CharField(max_length=40, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    parent_event_id = models.IntegerField()
    venue_name = models.CharField(max_length=255)
    venue_addr1 = models.CharField(max_length=255)
    venue_addr2 = models.CharField(max_length=255, blank=True, null=True)
    venue_zip = models.CharField(max_length=16, blank=True, null=True)
    venue_city = models.CharField(max_length=64)
    venue_state_cd = models.CharField(max_length=100)
    venue_country = models.CharField(max_length=2)
    venue_directions = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    host_addr_addressee = models.CharField(max_length=255, blank=True, null=True)
    host_addr_addr1 = models.CharField(max_length=255, blank=True, null=True)
    host_addr_addr2 = models.CharField(max_length=255, blank=True, null=True)
    host_addr_zip = models.CharField(max_length=16, blank=True, null=True)
    host_addr_city = models.CharField(max_length=64, blank=True, null=True)
    host_addr_state_cd = models.CharField(max_length=100, blank=True, null=True)
    host_addr_country = models.CharField(max_length=2)
    host_receive_rsvp_emails = models.IntegerField()
    contact_phone = models.CharField(max_length=25, blank=True, null=True)
    public_phone = models.IntegerField()
    capacity = models.IntegerField()
    all_shifts_full = models.IntegerField()
    closed_msg = models.TextField(blank=True, null=True)
    attendee_visibility = models.IntegerField()
    attendee_require_phone = models.IntegerField()
    attendee_volunteer_show = models.IntegerField()
    attendee_volunteer_message = models.TextField()
    is_official = models.IntegerField(blank=True, null=True)
    pledge_override_type = models.IntegerField()
    pledge_show = models.IntegerField()
    pledge_source = models.CharField(max_length=128, blank=True, null=True)
    pledge_subsource = models.CharField(max_length=128, blank=True, null=True)
    pledge_require = models.IntegerField()
    pledge_min = models.FloatField(blank=True, null=True)
    pledge_max = models.FloatField(blank=True, null=True)
    pledge_suggest = models.FloatField(blank=True, null=True)
    rsvp_use_default_email_message = models.IntegerField(blank=True, null=True)
    rsvp_email_message = models.TextField(blank=True, null=True)
    rsvp_email_message_html = models.TextField(blank=True, null=True)
    rsvp_use_reminder_email = models.IntegerField()
    rsvp_reminder_email_sent = models.IntegerField()
    rsvp_email_reminder_hours = models.IntegerField(blank=True, null=True)
    rsvp_allow = models.IntegerField(blank=True, null=True)
    rsvp_require_signup = models.IntegerField(blank=True, null=True)
    rsvp_disallow_account = models.IntegerField(blank=True, null=True)
    rsvp_reason = models.TextField(blank=True, null=True)
    rsvp_redirect_url = models.CharField(max_length=255)
    is_searchable = models.IntegerField()
    flag_approval = models.IntegerField()
    chapter = models.ForeignKey(Chapter)
    create_dt = models.DateTimeField(blank=True, null=True)
    create_app = models.CharField(max_length=128, blank=True, null=True)
    create_user = models.CharField(max_length=128, blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
    modified_app = models.CharField(max_length=128, blank=True, null=True)
    modified_user = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)
    objects = OurRevolutionObjectManager()
    
    def __unicode__(self):
        return self.name
    
    def get_api_data(self):
        data = super(Event, self).get_api_data()
        # hack
        data['attendee_visibility'] = 'COUNT'
        return data
    

    def get_api_endpoint(self):
        path = "create_event"
        if self.pk:
            path = "update_event"
        return "/event/%s" % path

    def save(self, *args, **kwargs):
        try:
            save_call = super(Event, self).save(*args, **kwargs)
        except:
            import ipdb; ipdb.set_trace()

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

