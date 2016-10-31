from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from bsd.auth import Constituent


class IndexView(TemplateView):
    template_name = 'splash.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, Constituent):
            return redirect('events-list')
        return super(IndexView, self).get(request, *args, **kwargs)
        