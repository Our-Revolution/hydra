import base64
import importlib
import json

from django import forms
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.module_loading import import_string

from espresso.models import Drip, SentDrip, QuerySetRule
from espresso.drips import DripBase
from espresso.utils import get_simple_fields #, get_user_model
from espresso.messages import DripMessage


class QuerySetRuleInlineAdminForm(forms.ModelForm):
    
    class Meta:
        model = QuerySetRule
        fields = '__all__'
        widgets = {
            'field_name': admin.widgets.AdminTextInputWidget(attrs={'autocomplete': "off"}),
            'field_value': admin.widgets.AdminTextInputWidget(attrs={'autocomplete': "off"})
        }


class QuerySetRuleInline(admin.TabularInline):
    model = QuerySetRule
    form = QuerySetRuleInlineAdminForm



class DripAdminForm(forms.ModelForm):
    
    class Meta:
        model = Drip
        fields = '__all__'
        widgets = {
            'name': admin.widgets.AdminTextInputWidget(attrs={'class': 'vLargeTextField'}),
            'from_email': admin.widgets.AdminTextInputWidget(attrs={'class': 'vLargeTextField'}),
            'from_email_name': admin.widgets.AdminTextInputWidget(attrs={'class': 'vLargeTextField'}),
            'subject_template': admin.widgets.AdminTextInputWidget(attrs={'class': 'vLargeTextField'}),
            'body_html_template': admin.widgets.AdminTextareaWidget(attrs={'class': 'vLargeTextField', 'rows': 20}),
            'description': admin.widgets.AdminTextInputWidget(attrs={'class': 'vLargeTextField'}),
        }


@admin.register(Drip)
class DripAdmin(admin.ModelAdmin):
    form = DripAdminForm
    inlines = [QuerySetRuleInline]
    list_display = ('name', 'enabled', 'description')
    save_as = True

    def send_sample_email(self, request, object_id, extra_context):
        drip = Drip.objects.get(pk=object_id)
        drip.drip.send_sample(request.user.email)
        self.message_user(request, "Sent to %s" % request.user.email, level='success')

    def change_view(self, request, object_id, extra_context=None):        
        default = super(ModelAdmin, self).change_view(request, object_id, extra_context)
        if '_email_to_me' in request.POST:
            self.send_sample_email(request, object_id, extra_context=extra_context)
        return default

    def populate_target_registry(self):
        registry = []
        for app in settings.INSTALLED_APPS:
            try:
                drip_emails = importlib.import_module("%s.drip_emails" % app)
                registry += [("%s.%s" % (cls.__module__, cls.__name__), cls.Meta.verbose_name) for name, cls in drip_emails.__dict__.items() if isinstance(cls, type) and issubclass(cls, DripBase)]
            except ImportError:
                pass
        self._target_registry = tuple(registry)

    av = lambda self, view: self.admin_site.admin_view(view)
    def timeline(self, request, drip_id, into_past, into_future):
        """
        Return a list of people who should get emails.
        """
        from django.shortcuts import render, get_object_or_404

        drip = get_object_or_404(Drip, id=drip_id)

        shifted_drips = []
        seen_users = set()
        for shifted_drip in drip.drip.walk(into_past=int(into_past), into_future=int(into_future)+1):
            shifted_drip.prune()
            shifted_drips.append({
                'drip': shifted_drip,
                'qs': shifted_drip.get_queryset().exclude(pk__in=seen_users)
            })
            seen_users.update(shifted_drip.get_queryset().values_list('pk', flat=True))

        return render(request, 'drip/timeline.html', locals())

    def view_drip_email(self, request, drip_id, into_past, into_future, item_id):
        from django.shortcuts import render, get_object_or_404
        from django.http import HttpResponse
        drip = get_object_or_404(Drip, id=drip_id)
        klass = import_string(drip.target).Meta.model
        item = get_object_or_404(klass, pk=item_id)
        context = import_string(drip.target).get_email_context(item)
        drip_message = DripMessage(drip.drip).set_context(context)

        html = ''
        mime = ''
        if drip_message.message.alternatives:
            for body, mime in drip_message.message.alternatives:
                if mime == 'text/html':
                    if drip.template:
                        html = render_to_string(drip.template, dict(context, **{'email_content': body}))
                    else:
                        html = body
                    mime = 'text/html'
        else:
            html = drip_message.message.body
            mime = 'text/plain'

        return HttpResponse(html, content_type=mime)

    def build_extra_context(self, extra_context, object_id=None):
        self.populate_target_registry()
        extra_context = extra_context or {}
        field_data = {}
        for item in self._target_registry:
            model = import_string(item[0])
            field_data[item[0]] = get_simple_fields(model.Meta.model)
        extra_context['field_data'] = json.dumps(field_data)
        self.model._meta.get_field('target').choices = self._target_registry
        return extra_context

    def add_view(self, request, extra_context=None):
        return super(DripAdmin, self).add_view(
            request, extra_context=self.build_extra_context(extra_context))

    def change_view(self, request, object_id, extra_context=None):
        return super(DripAdmin, self).change_view(
            request, object_id, extra_context=self.build_extra_context(extra_context, object_id=object_id))

    def get_urls(self):
        from django.conf.urls import url
        urls = super(DripAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<drip_id>[\d]+)/timeline/(?P<into_past>[\d]+)/(?P<into_future>[\d]+)/$',
                self.av(self.timeline),
                name='drip_timeline'
            ),
            url(
                r'^(?P<drip_id>[\d]+)/timeline/(?P<into_past>[\d]+)/(?P<into_future>[\d]+)/(?P<item_id>[\d]+)/$',
                self.av(self.view_drip_email),
                name='view_drip_email'
            )
        ]
        return my_urls + urls


@admin.register(SentDrip)
class SentDripAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SentDrip._meta.fields]
    ordering = ['-id']
