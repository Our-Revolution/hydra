from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from .forms import EventForm
from .models import Chapter, Event, EventType, OUR_REVOLUTION_CHAPTER_ID
from .auth import Constituent
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
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.has_perm('bsd.can_edit_own_%ss' % self.model._meta.verbose_name.lower(), obj=self.get_object()):
            return super(EventEdit, self).dispatch(*args, **kwargs)
        return render(self.request, "unauthorized.html", {'object_type': self.model._meta.verbose_name.lower()}, status=401)
    
#     def get(self, *args, **kwargs):
#         print "yo"
#         obj = self.get_object()
#         timezone.activate(obj.start_tz)
#         return super(EventEdit, self).get(*args, **kwargs)
#         
    
    def form_valid(self, form):
        #
        return super(EventEdit, self).form_valid(form)