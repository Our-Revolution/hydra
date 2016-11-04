from django.contrib import admin
from .auth import Constituent
from .models import Event, EventType
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


@admin.register(Constituent)
class ConstituentAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'userid']
    search_fields = ['firstname', 'lastname', 'userid']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_day']
    search_fields = ['name', 'venue_city']
    raw_id_fields = ['creator_cons', 'chapter']
    
    def response_change(self, request, obj):
        default = super(EventAdmin, self).response_change(request, obj)
        if "_continue" in request.POST:
            # events get a new ID on each API hit, so...
            new_pk = obj.__class__.objects.get(event_id_obfuscated=obj.event_id_obfuscated).pk
            preserved_filters = self.get_preserved_filters(request)
            redirect_url = reverse('admin:%s_%s_change' %(obj._meta.app_label,  obj._meta.model_name),  args=[new_pk] )
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': self.model._meta}, redirect_url)
            return HttpResponseRedirect(redirect_url)
        return default


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
