from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^events?/', include([
        url(r'^edit/(?P<pk>[0-9]+)$', views.EventEdit.as_view()),
        url(r'^create$', views.EventCreate.as_view()),
    ]))
]
