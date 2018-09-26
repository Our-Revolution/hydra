from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from . import views
import debug_toolbar

REDIRECT_EVENTS_URL = settings.REDIRECT_EVENTS_URL

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=REDIRECT_EVENTS_URL), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/blast-email', views.BlastEmail.as_view(), name='blast-email'),
    url(r'^admin/geo-target', views.GeoTarget.as_view(), name='geo-target'),
    url(r'', include('bsd.urls')),
    url(r'', include('chowda.urls')),
    url(
        r'^login/',
        RedirectView.as_view(url=REDIRECT_EVENTS_URL),
        name='login',
    ),
    url('^', include('django.contrib.auth.urls')),
]


if settings.DEBUG:
    urlpatterns.insert(0, url(r'^__debug__/', include(debug_toolbar.urls)))


admin.site.site_header = "Hydra administration"
