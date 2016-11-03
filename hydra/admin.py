# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.db.models import Prefetch
from django.template import Context, Template
from .models import EventPromotionRequest, ZipCode
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

    def __init__(self, *args, **kwargs):

        instance = kwargs.get('instance', None)

        if instance and not instance.sender_email:
            instance.message = Template("""Hi --

Our event host, {{ instance.event.creator_cons.firstname }} is hosting an event and is hoping
to get some more attendees —— would you be able to attend?

Thanks!


---------- Forwarded message ----------
From: {{ instance.event.creator_cons.email }}
Subject: {{ instance.subject }}

{{ instance.message }}""").render(Context({'instance': instance }))

        kwargs.update(instance=instance)

        super(EventPromotionRequestAdminForm, self).__init__(*args, **kwargs)



@admin.register(EventPromotionRequest)
class EventPromotionRequestAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_type', 'host_name', 'submitted', 'status']
    raw_id_fields = ['event', 'host', 'recipients']
    form = EventPromotionRequestAdminForm

    def save_model(self, request, obj, form, change):
        save_kwargs = {}
        if form.cleaned_data.get('send_preview_email_to', False):
            save_kwargs['preview'] = form.cleaned_data['send_preview_email_to']
        obj.save(**save_kwargs)
    
    def get_object(self, request, object_id, from_field=None):
        obj = super(EventPromotionRequestAdmin, self).get_object(request, object_id)
        if obj is not None:
            if not obj.sender_display_name:
                obj.sender_display_name = request.user.get_full_name()
            if not obj.sender_email:
                obj.sender_email = request.user.email
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