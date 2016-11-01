from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def clean_spaces(value):
    return mark_safe(" ".join(value.split('&nbsp;')))