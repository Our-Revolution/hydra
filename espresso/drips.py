import functools
import datetime
import logging
import operator
import pytz

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.module_loading import import_string
from espresso.messages import DripMessage


logger = logging.getLogger(__name__)


class DripBase(object):
    """
    A base object for defining a Drip.

    You can extend this manually, or you can create full querysets
    and templates from the admin.
    """
    #: needs a unique name
    name = None
    subject_template = None
    body_template = None
    from_email = None
    from_email_name = None
    template = None

    def __init__(self, drip_model, *args, **kwargs):
        self.drip_model = drip_model

        self.name = kwargs.pop('name', self.name)
        self.from_email = kwargs.pop('from_email', self.from_email)
        self.from_email_name = kwargs.pop('from_email_name', self.from_email_name)
        self.subject_template = kwargs.pop('subject_template', self.subject_template)
        self.body_template = kwargs.pop('body_template', self.body_template)
        self.template = kwargs.pop('template', self.template)

        if not self.name:
            raise AttributeError('You must define a name.')

        self.now_shift_kwargs = kwargs.get('now_shift_kwargs', {})

    #########################
    ### DATE MANIPULATION ###
    #########################

    def now(self):
        """
        This allows us to override what we consider "now", making it easy
        to build timelines of who gets what when.
        """
        return datetime.datetime.now(pytz.timezone('UTC'))

    def timedelta(self, *a, **kw):
        """
        If needed, this allows us the ability to manipuate the slicing of time.
        """
        from datetime import timedelta
        return timedelta(*a, **kw)

    def walk(self, into_past=0, into_future=0):
        """
        Walk over a date range and create new instances of self with new ranges.
        """
        walked_range = []
        for shift in range(-into_past, into_future):
            kwargs = dict(drip_model=self.drip_model,
                          name=self.name,
                          now_shift_kwargs={'days': shift})
            walked_range.append(self.__class__(**kwargs))
        return walked_range

    def apply_queryset_rules(self, qs):
        """
        First collect all filter/exclude kwargs and apply any annotations.
        Then apply all filters at once, and all excludes at once.
        """
        clauses = {
            'filter': [],
            'exclude': []}

        for rule in self.drip_model.queryset_rules.all():

            clause = clauses.get(rule.method_type, clauses['filter'])

            kwargs = rule.filter_kwargs(qs, now=self.now)
            clause.append(Q(**kwargs))

            qs = rule.apply_any_annotation(qs)

        if clauses['exclude']:
            qs = qs.exclude(functools.reduce(operator.or_, clauses['exclude']))
        qs = qs.filter(*clauses['filter'])

        if self.drip_model.ordering:
            qs = qs.order_by(**self.drip_model.ordering.split(','))

        if self.drip_model.limit > 0:
            qs = qs[0:self.drip_model.limit]

        return qs

    ##################
    ### MANAGEMENT ###
    ##################

    def get_queryset(self):
        try:
            return self._queryset
        except AttributeError:
            self._queryset = self.apply_queryset_rules(self.queryset())\
                                 .distinct()
            return self._queryset

    def run(self):
        """
        Get the queryset, prune sent people, and send it.
        """
        if not self.drip_model.enabled:
            return None

        self.prune()
        count = self.send()

        return count

    def send_sample(self, to):
        self.prune()
        count = self.send(to)
        return count

    def prune(self, count='all'):

        """
        Do an exclude for all Users who have a SentDrip already.
        """
        from espresso.models import SentDrip

        item_ids = list(self.get_queryset().values_list('pk', flat=True))
        exclude_ids = SentDrip.objects.filter(created__lt=datetime.datetime.now(),
                                                   drip=self.drip_model,
                                                   item_id__in=item_ids)\
                                           .values_list('item_id', flat=True)
        self._queryset = self.get_queryset().exclude(pk__in=list(exclude_ids))

        if count != 'all':
            self._queryset = self._queryset[0]

    def send(self, to=None):
        """
        Send the message to each user on the queryset.

        Create SentDrip for each user that gets a message.

        Returns count of created SentDrips.
        """

        from espresso.models import SentDrip

        if not self.from_email:
            self.from_email = getattr(settings, 'DRIP_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)

        count = 0
        for item in self.get_queryset():

            context = import_string(self.drip_model.target).get_email_context(item)
            if to:
                context['email_address'] = to
            
            message_instance = DripMessage(self).set_context(context)
            try:
                result = message_instance.message.send()
                if result and not to:
                    SentDrip.objects.create(
                        drip=self.drip_model,
                        item_id=item.pk,
                        from_email=self.from_email,
                        from_email_name=self.from_email_name,
                        subject=message_instance.subject,
                        body=message_instance.body
                    )
                count += 1
            except Exception as e:
                logger.error("Failed to send drip %s to %s: %s" % (self.drip_model.id, message_instance.context['email_address'], e))
                
            if to:
                break

        return count


    ####################
    ### USER DEFINED ###
    ####################

    def queryset(self):
        """
        Returns a queryset of auth.User who meet the
        criteria of the drip.

        Alternatively, you could create Drips on the fly
        using a queryset builder from the admin interface...
        """
        klass = import_string(self.drip_model.target).Meta.model
        return klass.objects.select_related()

