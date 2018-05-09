# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context, Template
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView, FormView, UpdateView, ModelFormMixin
from django.views.generic.list import ListView
from .decorators import bsd_login_required, class_view_decorator
from .forms import EventForm, EventPromoteForm
from .models import Chapter, Event, EventType, OUR_REVOLUTION_CHAPTER_ID
from .auth import Constituent
from hydra.models import EventPromotionRequest
import datetime
import logging

logger = logging.getLogger(__name__)


@class_view_decorator(bsd_login_required)
class EventsView(ListView):
    model = Event
    template_name = "event_list.html"

    def get_queryset(self):
        logger.debug(self.request.user)
        logger.debug(Event.objects.filter(creator_cons=self.request.user, start_day__gte=datetime.date.today()))
        return Event.objects.filter(creator_cons=self.request.user, start_day__gte=datetime.date.today())

    def get_context_data(self, *args, **kwargs):
        context = super(EventsView, self).get_context_data(*args, **kwargs)
        context['past_events'] = Event.objects.filter(creator_cons=self.request.user, start_day__lt=datetime.date.today())
        logger.debug(context)
        return context

@class_view_decorator(bsd_login_required)
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

        if self.request.user.is_authenticated:
            initial['creator_cons'] = self.request.user.pk
            initial['creator_name'] = ' '.join([self.request.user.firstname, self.request.user.lastname])

        return initial

    def form_valid(self, form):
        try:
            self.object = form.save()
            messages.add_message(self.request, messages.SUCCESS, "Your event has been created.")
            return super(ModelFormMixin, self).form_valid(form)

        except BaseException, e:
            if hasattr(e, '__iter__'):
                for exc in e:
                    messages.add_message(self.request, messages.ERROR, "Error creating your event -- %s" % exc[1][0])
                    if hasattr(form, exc[0]):
                        form.add_error(exc[0], exc[1][0])
            elif isinstance(e, UnicodeError):
                field =  e[1][e[1][0:e[3]].rfind('&')+1:e[1][0:e[3]].rfind('=')]
                messages.add_message(self.request, messages.ERROR, "Error creating your event -- You had some special characters in your %s field, please remove those and try again." % field)
                if field in form.fields:
                    form.add_error(field, "Please remove special characters and try again.")
            return super(EventCreate, self).form_invalid(form)

    def form_invalid(self, form):
        return super(EventCreate, self).form_invalid(form)


class EventCreatorMixin(object):

    def get_object(self):
        if not hasattr(self, '_object'):
            self._object = super(EventCreatorMixin, self).get_object()
        return self._object

    @method_decorator(bsd_login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.has_perm('bsd.can_edit_own_%ss' % self.model._meta.verbose_name.lower(), obj=self.get_object()):
            return super(EventCreatorMixin, self).dispatch(*args, **kwargs)
        return render(self.request, "unauthorized.html", {'object_type': self.model._meta.verbose_name.lower()}, status=401)


@class_view_decorator(bsd_login_required)
class EventEdit(EventCreatorMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = '/events'

    def get_queryset(self):
        return Event.objects.select_related('creator_cons').all()


    def form_valid(self, form):
        try:
            self.object = form.save()
            messages.add_message(self.request, messages.SUCCESS, "Your event has been updated.")
            return super(ModelFormMixin, self).form_valid(form)

        except BaseException, e:
            if hasattr(e, '__iter__'):
                for exc in e:
                    messages.add_message(self.request, messages.ERROR, "Error creating your event -- %s" % exc[1][0])
                    if hasattr(form, exc[0]):
                        form.add_error(exc[0], exc[1][0])
            elif isinstance(e, UnicodeError):
                field =  e[1][e[1][0:e[3]].rfind('&')+1:e[1][0:e[3]].rfind('=')]
                if field in form.fields:
                    form.add_error(field, "Please remove special characters and try again.")
                messages.add_message(self.request, messages.ERROR, "Error updating your event -- You had some special characters in your %s field, please remove those and try again." % field)
            return super(EventEdit, self).form_invalid(form)


@class_view_decorator(bsd_login_required)
class EventPromote(EventCreatorMixin, CreateView):
    # hack for EventCreator permissions mixin
    model = Event

    # actual model is the request, as set on the form.
    form_class = EventPromoteForm
    success_url = "/events"
    template_name = "promote.html"

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.add_message(self.request, messages.ERROR, "Error submitting your request -- %s" % error)
        return super(EventPromote, self).form_invalid(form)


    def form_valid(self, form):
        default = super(EventPromote, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Your request has been submitted.")
        return default


    def get_initial(self, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])

        event_data = dict(event.__dict__)

        if not event_data.get('creator_name', None):
            event_data['creator_name'] = " ".join([event.creator_cons.firstname, event.creator_cons.lastname])

        return {
                    'event': event,
                    'volunteer_count': 4000 if event.capacity == 0 else event.capacity * 40,
                    'subject': "Please come to my %s event" % event.event_type.name,
                    'message': Template("""Hello --

I'm hoping to get more attendees at my event, {{ event.name }}! Can you make it? We're almost across the finish line and we need to keep up the momentum.


Thanks!


{{ event.creator_cons.firstname }}""").render(Context({'event': event}))
                }
