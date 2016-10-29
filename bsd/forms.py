from django import forms
from .models import Event
from .widgets import *


class EventForm(forms.ModelForm):
	
	class Meta:
		exclude = ['event_id_obfuscated', 'contribution_page_id', 'outreach_page_id', \
					'parent_event_id', 'latitude', 'longitude', 'host_addr_addressee', \
					'host_addr_addr1', 'host_addr_addr2', 'host_addr_zip', 'host_addr_city', \
					'host_addr_state_cd', 'host_addr_country', 'pledge_override_type', 'pledge_show', \
					'pledge_source', 'pledge_subsource', 'pledge_require', 'pledge_min', \
					'pledge_max', 'pledge_suggest', 'all_shifts_full', 'closed_msg', \
					'rsvp_email_message', 'rsvp_email_message_html', 'attendee_visibility', \
					'attendee_require_phone', 'attendee_volunteer_show', 'attendee_volunteer_message', \
					'rsvp_use_default_email', 'rsvp_reminder_email_sent', 'rsvp_use_default_email_message', \
					'rsvp_allow', 'rsvp_require_signup', 'rsvp_disallow_account', 'rsvp_reason', \
					'rsvp_redirect_url', 'flag_approval', 'create_dt', 'create_app', 'create_user',
					'modified_dt', 'modified_app', 'modified_user', 'status', 'note', 'is_visible', \
					'is_official', 'is_searchable', 'rsvp_use_reminder_email', \
					'rsvp_email_reminder_hours', 'start_dt']
		model = Event
		widgets = {
			'host_receive_rsvp_emails': forms.widgets.CheckboxInput(),
			'public_phone': forms.widgets.CheckboxInput(),
			'creator_cons': forms.widgets.HiddenInput(),
			'chapter': forms.widgets.HiddenInput(),
			'venue_directions': forms.widgets.Textarea(attrs={'rows': 3}),
			'description': forms.widgets.Textarea(attrs={'rows': 5}),
			
			# html5
			'start_day': HTML5DateInput(),
			'start_time': HTML5TimeInput(),
		}