from django import forms
from django.utils.html import format_html, format_html_join, smart_urlquote
from django.utils.safestring import mark_safe



class GroupIdWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        output = [super(GroupIdWidget, self).render(name, value, attrs)]

        key = self.rel.get_related_field().name
        try:

            obj = self.rel.model._default_manager.using(self.db).get(**{key: value})
            
            # add front-end and back-end link
            output.append("<a href=\"https://ourrevolution.com/groups/%s\">Group Page</a>" % obj.slug)
            output.append(" | <a href=\"https://ourrevolution.com/admin/local_groups/group/%s/change/\">Admin</a>" % obj.pk)

        except (ValueError, self.rel.model.DoesNotExist):
            pass

        return mark_safe(''.join(output))