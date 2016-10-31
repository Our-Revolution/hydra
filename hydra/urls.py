from django.conf.urls import include, url
from django.contrib import admin
from . import views
import debug_toolbar

urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'', include('bsd.urls')),
    url('^', include('django.contrib.auth.urls')),
]


admin.site.site_header = "Hydra administration"