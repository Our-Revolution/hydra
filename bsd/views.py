from django.views.generic.edit import CreateView, UpdateView
from .forms import EventForm
from .models import Chapter, Constituent, Event, OUR_REVOLUTION_CHAPTER_ID



class EventCreate(CreateView):
	model = Event
	form_class = EventForm
	template_name = "event_form.html"
	
	def get_initial(self, *args, **kwargs):
		return {
			'chapter': Chapter.objects.get(pk=OUR_REVOLUTION_CHAPTER_ID),
			'creator_cons': Constituent.objects.get(pk=927998)
		}

	def form_valid(self, form):
		#
		return super(EventView, self).form_valid(form)


class EventUpdate(UpdateView):
	model = Event
	form_class = EventForm
	template_name = 'event_form.html'
	success_url = '/'
		
	
	def get_initial(self, *args, **kwargs):
		return {
			'chapter': Chapter.objects.get(pk=OUR_REVOLUTION_CHAPTER_ID),
			'creator_cons': Constituent.objects.get(pk=927998)
		}
	
	
	def form_valid(self, form):
		#
		return super(EventView, self).form_valid(form)