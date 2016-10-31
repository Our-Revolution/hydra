from django.views.generic.base import TemplateView
# from bsd.decorators import bsd_login_required, class_view_decorator


# @class_view_decorator(bsd_login_required)
class IndexView(TemplateView):
    template_name = 'splash.html'