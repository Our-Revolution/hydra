# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib import messages
from django.db.models import Prefetch
from django.template import Context, Template
from pytz import timezone

from .models import EventPromotionRequest, ZipCode
from .widgets import GroupIdWidget
from bsd.models import Event, EventType
from bsd.auth import Constituent




class EventPromotionRequestAdminForm(forms.ModelForm):
    send_preview_email_to = forms.CharField(max_length=1024, help_text="Comma separated email addresses -- filling this out will ONLY send a preview.", required=False)
    
    class Meta:
        model = EventPromotionRequest
        fields = '__all__'
        widgets = {
            'subject': admin.widgets.AdminTextInputWidget(attrs={'style': "width: 610px"}),
            'message': admin.widgets.AdminTextareaWidget
        }


def mark_skipped(modeladmin, request, queryset):
    queryset.update(status='skipped')
mark_skipped.short_description = "Mark selected requests as skipped"


@admin.register(EventPromotionRequest)
class EventPromotionRequestAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date', 'host_name', 'volunteer_count', 'submitted', 'status']
    raw_id_fields = ['event', 'host', 'recipients',]
    form = EventPromotionRequestAdminForm
    list_filter = ['status']
    actions = [mark_skipped]

    def event_date(self, obj):
        return obj.event.start_dt.astimezone(timezone(obj.event.start_tz)).strftime("%a, %b%e, %l:%M%P %Z")

    def save_model(self, request, obj, form, change):
        save_kwargs = {}
        if form.cleaned_data.get('send_preview_email_to', False):
            save_kwargs['preview'] = form.cleaned_data['send_preview_email_to']
        try:
            obj.save(**save_kwargs)
        except ValueError, e:
            self.message_user(request, "Error sending out promotion blast -- %s" % e.message, level=messages.ERROR)


    def view_on_site(self, obj):
        return obj.event.get_absolute_url()
    
    def get_object(self, request, object_id, from_field=None):
        obj = super(EventPromotionRequestAdmin, self).get_object(request, object_id)
        if obj is not None:
            first_name = request.user.first_name
            if not obj.sender_display_name:
                obj.sender_display_name = "%s - Our Revolution" % first_name
            if not obj.sender_email:
                obj.subject = "Fwd: " + obj.subject
                obj.message = Template("""Hi --

Your neighbor {{ obj.event.creator_cons.firstname }} is hosting an event and is hoping
to get some more attendees —— would you be able to attend?

Learn more or RSVP here: {{ obj.event.get_absolute_url }}

Thanks!

{{ first_name }}
Our Revolution


---------- Forwarded message ----------
Subject: {{ obj.subject }}

{{ obj.message }}


----
Paid for by Our Revolution
(not the billionaires)

603 2ND STREET NE - WASHINGTON, DC 20002

Email is one of the most important tools we have to reach supporters like you, but if you’d like to, click here to unsubscribe: https://go.ourrevolution.com/page/unsubscribe/""").render(Context({'obj': obj, 'first_name': first_name }))
            if not obj.sender_email:
                obj.sender_email = "info@ourrevolution.com"
        return obj
    
    def get_queryset(self, request):
        return super(EventPromotionRequestAdmin, self).get_queryset(request).prefetch_related(Prefetch('event', Event.objects.all()), Prefetch('host', Constituent.objects.all()), Prefetch('event__event_type', EventType.objects.all()))
    
    def event_name(self, obj):
        return obj.event.name
        
    def event_type(self, obj):
        return obj.event.event_type
        
    def host_name(self, obj):
        return obj.event.creator_name
        
        
@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    search_fields = ['zip']
    list_display = ['zip']
