from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView
from .forms import EventForm
from .models import Chapter, Constituent, Event, EventType, OUR_REVOLUTION_CHAPTER_ID
import datetime




class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = '/'
    
    def get_initial(self, *args, **kwargs):
        return {
            # sane defaults
            'chapter': Chapter.objects.get(pk=OUR_REVOLUTION_CHAPTER_ID),
            'duration': 4,
            'duration_unit': 60,
            
            'name': "Canvassing for Our Revolution",
            'event_type': EventType.objects.get(name="Canvass for Our Revolution"),
            'description': "Test description",
            
            'start_day': datetime.date.today(),
            'start_time': datetime.datetime.time(datetime.datetime.now()),
            
            'capacity': 0,
            'host_receive_rsvp_emails': 1,
            'public_phone': 1,
            
            
            # JUST FOR DEBUG PURPOSES
            'creator_cons': Constituent.objects.get(pk=927998),
            'creator_name': "Jon Culver",
            'start_tz': "America/Los_Angeles",
            'venue_name': "Culver House",
            'venue_addr1': "19521 44th Ave NE",
            'venue_city': "Lake Forest Park",
            'venue_state_cd': "WA",
            'venue_zip': "98155",
            'venue_country': "US",
            'contact_phone': "502-807-1976",
        }

    def form_valid(self, form):
        #
        return super(EventCreate, self).form_valid(form)


class EventEdit(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = '/'
    
    def get(self, *args, **kwargs):
        print "yo"
        obj = self.get_object()
        timezone.activate(obj.start_tz)
        return super(EventEdit, self).get(*args, **kwargs)
        
    
    def form_valid(self, form):
        #
        return super(EventEdit, self).form_valid(form)