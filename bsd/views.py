from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView, FormView, UpdateView
from .forms import EventForm, EventPromoteForm
from .models import Chapter, Event, EventType, OUR_REVOLUTION_CHAPTER_ID
from .auth import Constituent
import datetime




class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = '/'
    
    def get_initial(self, *args, **kwargs):
        
        initial = {
            'chapter': Chapter.objects.get(pk=OUR_REVOLUTION_CHAPTER_ID),
            'start_day': datetime.date.today() + datetime.timedelta(days=4),
            'start_time': datetime.time(hour=17, minute=0, second=0),
            'capacity': 0,
            'host_receive_rsvp_emails': 1,
            'public_phone': 1,
        }
        
        if self.request.user.is_authenticated():
            initial['creator_cons'] = self.request.user.pk
            initial['creator_name'] = ' '.join([self.request.user.firstname, self.request.user.lastname])
        
        return initial

    def form_valid(self, form):
        #
        return super(EventCreate, self).form_valid(form)
        
        
class EventCreatorMixin(object):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.has_perm('bsd.can_edit_own_%ss' % self.model._meta.verbose_name.lower(), obj=self.get_object()):
            return super(EventCreatorMixin, self).dispatch(*args, **kwargs)
        return render(self.request, "unauthorized.html", {'object_type': self.model._meta.verbose_name.lower()}, status=401)



class EventEdit(EventCreatorMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = '/events'
    
    

class EventPromote(SingleObjectTemplateResponseMixin, SingleObjectMixin, EventCreatorMixin, FormView):
    model = Event
    form_class = EventPromoteForm
    success_url = "/events"
    template_name = "promote.html"
    
    def get_initial(self, *args, **kwargs):
        print self.object
        return {
                    'volunteer_count': 100 if self.object.capacity == 0 else self.object.capacity * 2,
                    'subject': "Please come to my %s event" % self.object.event_type.name,
                    'message': """Hello --
                    
I'm hoping to get more attendees at my event, %(name)s. Could you please come?

Thanks!

%(creator_name)s""" % dict(self.object.__dict__)}
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EventPromote, self).get(request, *args, **kwargs)