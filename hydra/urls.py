from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from . import views
import debug_toolbar

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/blast-email', views.BlastEmail.as_view(), name='blast-email'),
    url(r'', include('bsd.urls')),
    url('^', include('django.contrib.auth.urls')),
]


if settings.DEBUG:
    urlpatterns.insert(0, url(r'^__debug__/', include(debug_toolbar.urls)))


admin.site.site_header = "Hydra administration"