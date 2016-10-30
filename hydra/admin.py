from django import forms
from django.contrib import admin
from django.db.models import Prefetch
from .models import EventPromotionRequest, ZipCode
from bsd.models import Event, EventType
from bsd.auth import Constituent



class EventPromotionRequestAdminForm(forms.ModelForm):
    
    class Meta:
        model = EventPromotionRequest
        fields = '__all__'
        widgets = {
            'subject': admin.widgets.AdminTextInputWidget(attrs={'style': "width: 610px"}),
            'message': admin.widgets.AdminTextareaWidget
        }


@admin.register(EventPromotionRequest)
class EventPromotionRequestAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_type', 'host_name', 'submitted', 'status']
    raw_id_fields = ['event', 'host', 'recipients']
    form = EventPromotionRequestAdminForm
    
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