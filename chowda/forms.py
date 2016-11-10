from django import forms
from django.utils.html import format_html, mark_safe
from django.utils.encoding import force_text
from .models import Slack


class CheckboxFieldRendererWithDescription(forms.widgets.CheckboxFieldRenderer):

    def render(self):
        id_ = self.attrs.get('id')
        output = []
        descriptions = dict(Slack.objects.values_list('id', 'description'))
        for i, choice in enumerate(self.choices):
            choice_value, choice_label = choice
            w = self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, i)
            output.append(format_html(self.inner_html, choice_value=force_text(w), sub_widgets=mark_safe(format_html('<p>{}</p>', descriptions[choice_value]))))
        return format_html(
            self.outer_html,
            id_attr=format_html(' id="{}"', id_) if id_ else '',
            content=mark_safe('\n'.join(output)),
        )



class SlackInviteForm(forms.Form):
    email = forms.EmailField()
    slack = forms.ModelMultipleChoiceField(queryset=Slack.objects.all(), widget=forms.widgets.CheckboxSelectMultiple(renderer=CheckboxFieldRendererWithDescription))