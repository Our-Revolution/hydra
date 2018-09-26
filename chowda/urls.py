from django.conf import settings
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from . import views

REDIRECT_SLACK_URL = settings.REDIRECT_SLACK_URL

urlpatterns = [
    url(
        r'^join-us-on-slack$',
        RedirectView.as_view(url=REDIRECT_SLACK_URL),
        name='slack-invite'
    )
]
