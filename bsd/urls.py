from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^events?/', include([
        url(r'^(?P<pk>[0-9]+)/edit$', views.EventEdit.as_view(), name="event-edit"),
        url(r'^(?P<pk>[0-9]+)/promote$', views.EventPromote.as_view(), name="event-promote"),
        url(r'^create$', views.EventCreate.as_view(), name="event-create"),
    ]))
]
