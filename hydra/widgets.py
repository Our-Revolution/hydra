from django import forms
from django.utils.html import format_html, format_html_join, smart_urlquote
from django.utils.safestring import mark_safe
from groups.models import Group
import logging


class GroupIdWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        output = [super(GroupIdWidget, self).render(name, value, attrs)]

        try:
            obj = Group.objects.get(group_id=value)
            logging.debug(value)
            logging.debug(obj)
            logging.debug(obj.pk)
            logging.debug(obj.name)
            logging.debug(obj.slug)

            output.append("<strong style=\"margin-left: 1em\">%s</strong>" % obj.name)
            
            # add front-end and back-end link
            output.append("<span style=\"margin-left: 1em;\"><a href=\"https://ourrevolution.com/groups/%s\" target=\"_blank\">Group Page</a>" % obj.slug)
            output.append(" | <a href=\"https://ourrevolution.com/admin/local_groups/group/%s/change/\" target=\"_blank\">Admin</a></span>" % obj.pk)

        except (ValueError, self.rel.model.DoesNotExist):
            pass

        return mark_safe(''.join(output))
