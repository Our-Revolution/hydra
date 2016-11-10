from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^join-us-on-slack$', views.SlackInviteFormView.as_view(), name='slack-invite')
]