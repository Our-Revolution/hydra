from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

from .drips import DripBase
from .helpers import parse


class Drip(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Drip Name',
                                help_text='A unique name for this drip.')
    from_email_name = models.CharField(max_length=150, null=True, blank=True,
                                help_text="Set a name for a custom from email.")
    from_email = models.EmailField(null=True, blank=True,
                                help_text='Set a custom from email.')
    subject_template = models.TextField(null=True, blank=True)
    body_html_template = models.TextField(null=True, blank=True,
                                help_text='You will have settings and user in the context.')
    template = models.CharField(max_length=64, null=True, blank=True, default=None, choices=settings.DRIP_TEMPLATES)
    target = models.CharField(max_length=128, null=True, blank=True)
    limit = models.IntegerField(default=0, help_text="Leave 0 to fetch all objects.")
    ordering = models.CharField(max_length=128, null=True, blank=True, help_text="Only used if you specify a limit. If so, by what criteria should we choose which objects make the cut?")
    enabled = models.BooleanField(default=False)
    description = models.CharField(max_length=1024, blank=True, null=True, help_text="A line or two about what this does, and why. Good for institutional knowledge")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Drip Campaign'

    @property
    def drip(self):
        return DripBase(drip_model=self,
                        name=self.name,
                        from_email=self.from_email if self.from_email else None,
                        from_email_name=self.from_email_name if self.from_email_name else None,
                        subject_template=self.subject_template if self.subject_template else None,
                        body_template=self.body_html_template if self.body_html_template else None,
                        template=self.template if self.template else None)

    def get_target_model(self):
        return import_string(self.target).Meta.model

    def __unicode__(self):
        return self.name


class SentDrip(models.Model):
    """
    Keeps a record of all sent drips.
    """
    drip = models.ForeignKey('espresso.Drip', related_name='send_drips')
    item_id = models.BigIntegerField()
    subject = models.TextField()
    body = models.TextField()
    from_email = models.EmailField(null=True, default=None)
    from_email_name = models.CharField(max_length=150, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sent Drip Email'


METHOD_TYPES = (
    ('filter', 'Filter'),
    ('exclude', 'Exclude'),
)


LOOKUP_TYPES = (
    ('exact', 'exactly'),
    ('iexact', 'exactly (case insensitive)'),
    ('contains', 'contains'),
    ('icontains', 'contains (case insensitive)'),
    ('regex', 'regex'),
    ('iregex', 'contains (case insensitive)'),
    ('gt', 'greater than'),
    ('gte', 'greater than or equal to'),
    ('lt', 'less than'),
    ('lte', 'less than or equal to'),
    ('startswith', 'starts with'),
    ('endswith', 'starts with'),
    ('istartswith', 'ends with (case insensitive)'),
    ('iendswith', 'ends with (case insensitive)'),
)

class QuerySetRule(models.Model):
    drip = models.ForeignKey(Drip, related_name='queryset_rules')
    method_type = models.CharField(max_length=12, default='filter', choices=METHOD_TYPES, verbose_name='Type')
    field_name = models.CharField(max_length=128, verbose_name='Fields')
    lookup_type = models.CharField(max_length=12, default='exact', choices=LOOKUP_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    field_value = models.CharField(max_length=255, blank=True,
        help_text=('Can be anything from a number, to a string. Or, do ' +
                   '`now-7 days` or `today+3 days` for fancy timedelta.'))

    def clean(self):
        if not self.drip.target:
            return
        klass = self.drip.get_target_model()
        try:
            self.apply(klass.objects.all())
        except Exception as e:
            raise ValidationError(
                '%s raised trying to apply rule: %s' % (type(e).__name__, e))

    @property
    def annotated_field_name(self):
        field_name = self.field_name
        if field_name.endswith('__count'):
            agg, _, _ = field_name.rpartition('__')
            field_name = 'num_%s' % agg.replace('__', '_')
        elif field_name.endswith('__max'):
            agg, _, _ = field_name.rpartition('__')
            field_name = 'num_%s' % agg.replace('__', '_')

        return field_name

    def apply_any_annotation(self, qs):
        if self.field_name.endswith('__count'):
            field_name = self.annotated_field_name
            agg, _, _ = self.field_name.rpartition('__')
            qs = qs.annotate(**{field_name: models.Count(agg, distinct=True)})
        elif self.field_name.endswith('__max'):
            field_name = self.annotated_field_name
            agg, _, _ = self.field_name.rpartition('__')
            qs = qs.annotate(**{field_name: models.Max(agg, distinct=True)})
        return qs

    def filter_kwargs(self, qs, now=datetime.now):

        # Support Count() as m2m__count
        field_name = self.annotated_field_name
        field_name = '__'.join([field_name, self.lookup_type])
        field_value = self.field_value

        # set time deltas and dates
        if self.field_value == 'now':
            field_value = now()
        elif self.field_value == 'today':
            field_value = now().date()
        elif self.field_value.startswith('now-'):
            field_value = self.field_value.replace('now-', '')
            field_value = now() - parse(field_value)
        elif self.field_value.startswith('now+'):
            field_value = self.field_value.replace('now+', '')
            field_value = now() + parse(field_value)
        elif self.field_value.startswith('today-'):
            field_value = self.field_value.replace('today-', '')
            field_value = now().date() - parse(field_value)
        elif self.field_value.startswith('today+'):
            field_value = self.field_value.replace('today+', '')
            field_value = now().date() + parse(field_value)

        # F expressions
        if self.field_value.startswith('F_'):
            field_value = self.field_value.replace('F_', '')
            field_value = models.F(field_value)

        # set booleans
        if self.field_value == 'True':
            field_value = True
        if self.field_value == 'False':
            field_value = False

        kwargs = {field_name: field_value}

        return kwargs

    def apply(self, qs, now=datetime.now):
        kwargs = self.filter_kwargs(qs, now)
        qs = self.apply_any_annotation(qs)

        if self.method_type == 'filter':
            return qs.filter(**kwargs)
        elif self.method_type == 'exclude':
            return qs.exclude(**kwargs)

        # catch as default
        return qs.filter(**kwargs)

    class Meta:
        verbose_name = "Targeting Rule"
