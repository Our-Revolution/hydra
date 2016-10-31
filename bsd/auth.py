from bs4 import BeautifulSoup
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from .api import BSDModel
from .models import Event



class Constituent(BSDModel):
    API_ENCODING    = 'xml'
    
    is_authenticated = True
    
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
    
    def save(self, *args, **kwargs):
        
        # hack - signal from django.contrib.auth, we can ignore
        if kwargs == {'update_fields': ['last_login']}:
            return self
            
        return super(Constituent, self).save(*args, **kwargs)
        
        
    def has_perm(self, perm, obj=None):
        if perm == "bsd.can_edit_own_events":
            if isinstance(obj, Event) and obj.creator_cons == self:
                return True
        return False
        
        
    def has_perms(self, perm_list, obj=None):
        if perm_list == ["bsd.can_edit_own_events"]:
            if isinstance(obj, Event) and Event.creator_cons == self:
                return True
        return False
        
    def has_module_perms(self, package_name):
        # uhh...
        return False
        
    # glorious hack is glorious.
    @property
    def is_staff(self):
        STAFF_EMAILS = ['jon@ourrevolution.com', 'chris@ourrevolution.com', 'kyle@ourrevolution.com']
        return self.emails.filter(email__in=STAFF_EMAILS).exists()
        
    def get_username(self):
        return self.emails.order_by('-is_primary').first().email
     
    def is_active(self):
        # could flesh out more here.
        # also todo: superusers and things
        return self.is_validation == 1 and self.is_banned == 0

    def check_password(self, password):
        # there might be cleaner ways to implement this, but this covers
        # a lot of bases in terms of what response we need to see from BSD
        req = self._submit("/account/check_credentials", {'userid': self.userid, 'password': password })
        soup = BeautifulSoup(req.text, "xml")
        try:
            assert req.headers.get('Content-Type').startswith('application/xml')
            assert soup.find('cons') is not None
            assert soup.find('cons')['id'] == str(self.cons_id)
            assert soup.find('has_account').text == "1"
            assert soup.find('is_banned').text == "0"
            return True
        except AssertionError:
            return None

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)

    class Meta:
        managed = False
        db_table = 'cons'
        permissions = (
            ("can_edit_own_events", "Can edit own events"),
        )