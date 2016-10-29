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
            'chapter': Chapter.objects.get(pk=OUR_REVOLUTION_CHAPTER_ID),
            
            # JUST FOR DEBUG PURPOSES
            'creator_cons': Constituent.objects.get(pk=927998),
            'name': "Canvassing for Our Revolution",
            'event_type': EventType.objects.get(name="Canvass for Our Revolution"),
            'description': "Test description",
            'creator_name': "Jon Culver",
            'start_day': datetime.date.today(),
            'start_time': datetime.datetime.time(datetime.datetime.now()),
            'duration': 4,
            'duration_unit': 60,
            'start_tz': "America/Los_Angeles",
            'venue_name': "Culver House",
            'venue_addr1': "19521 44th Ave NE",
            'venue_city': "Lake Forest Park",
            'venue_state_cd': "WA",
            'venue_zip': "98155",
            'venue_country': "US",
            'contact_phone': "502-807-1976",
            'capacity': 0,
            'host_receive_rsvp_emails': 1,
            'public_phone': 1
        }

    def form_valid(self, form):
        #
        return super(EventCreate, self).form_valid(form)


class EventEdit(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = '/'
        
    
    def get_initial(self, *args, **kwargs):
        return {
            'chapter': Chapter.objects.get(pk=OUR_REVOLUTION_CHAPTER_ID),
            
            # JUST FOR DEBUG PURPOSES
            'creator_cons': Constituent.objects.get(pk=927998),
            'name': "Canvassing for Our Revolution",
            'event_type': EventType.objects.get(name="Canvass for Our Revolution"),
            'description': "Test description",
            'creator_name': "Jon Culver",
            'start_day': datetime.date.today(),
            'start_time': datetime.datetime.time(datetime.datetime.now()),
            'duration': 4,
            'duration_unit': 60,
            'start_tz': "America/Pacific",
            'venue_name': "Culver House",
            'venue_addr1': "19521 44th Ave NE",
            'venue_city': "Lake Forest Park",
            'venue_state_cd': "WA",
            'venue_zip': "98155",
            'venue_country': "US",
            'contact_phone': "502-807-1976",
            'capacity': 0
            
        }
    
    
    def form_valid(self, form):
        #
        return super(EventEdit, self).form_valid(form)