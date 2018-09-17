from django.conf import settings
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from . import views

REDIRECT_EVENTS_URL = settings.REDIRECT_EVENTS_URL

urlpatterns = [
    url(r'^events?/', include([
        url(
            r'^$',
            RedirectView.as_view(url=REDIRECT_EVENTS_URL),
            name="events-list"
        ),
        url(
            r'^(?P<pk>[0-9]+)/edit$',
            RedirectView.as_view(url=REDIRECT_EVENTS_URL),
            name="event-edit"
        ),
        url(
            r'^(?P<pk>[0-9]+)/promote$',
            RedirectView.as_view(url=REDIRECT_EVENTS_URL),
            name="event-promote"
        ),
        url(
            r'^create$',
            RedirectView.as_view(url=REDIRECT_EVENTS_URL),
            name="event-create"
        ),
    ]))
]
