import itertools
from django import forms
from .models import Event
from .auth import Constituent
from .widgets import *



class EventForm(forms.ModelForm):
    host_receive_rsvp_emails = forms.ChoiceField(choices=((1, "YES, please email me when new people RSVP (recommended)"), (0, "No thanks")), widget=forms.widgets.RadioSelect)
    public_phone = forms.ChoiceField(choices=((1, "YES, make my phone number visible to people viewing your event (recommended)"), (0, "Please keep my number private")), widget=forms.widgets.RadioSelect)
    duration = forms.IntegerField(widget=UnitsAndDurationWidget)
    creator_cons = forms.ModelChoiceField(queryset=Constituent.objects.none(), required=False, widget=forms.widgets.HiddenInput)
    
    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        cleaned_data['duration'] = int(cleaned_data['duration']) * int(cleaned_data['duration_unit'])
        return cleaned_data
    
    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        
        # super gross.
        creator_cons_lookup = self.initial['creator_cons']
        if isinstance(creator_cons_lookup, int):
            creator_cons_lookup = creator_cons_lookup.pk
        self.fields['creator_cons'].queryset = Constituent.objects.filter(pk=creator_cons_lookup)
        
        # minutes to hours. 30 == arbitrary
#         if self.instance:
#             if self.fields['duration'] > 30:
#                 self.fields['duration'].value = int(self.fields['duration'].value / 60)
#                 self.fields['duration_unit'].value = 60

    
    class Meta:
    
        # also, look into floppy and/or crispy forms
        fields = ['event_type', 'name', 'description', 'creator_name', 'creator_cons',        
                    'start_day', 'start_time', 'duration', 'start_tz',
                    'venue_name', 'venue_addr1', 'venue_addr2', 'venue_city',
                        'venue_state_cd', 'venue_zip', 'venue_country', 'venue_directions',
                    'host_receive_rsvp_emails', 'contact_phone', 'public_phone', 'capacity']

        model = Event

        widgets = {
            'creator_cons': forms.widgets.HiddenInput(),
            'chapter': forms.widgets.HiddenInput(),
            'venue_directions': forms.widgets.Textarea(attrs={'rows': 3}),
            'description': forms.widgets.Textarea(attrs={'rows': 5}),
            
            # html5
            'start_day': HTML5DateInput(),
            'start_time': HTML5TimeInput(),
        }