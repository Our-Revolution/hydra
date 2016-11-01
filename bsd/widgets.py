from django.forms import widgets
from .models import Event
from django.utils.safestring import mark_safe
from django.utils.html import format_html



class UnitsAndDurationWidget(widgets.MultiWidget):
    
    def __init__(self, attrs=None):
        _widgets = (
            widgets.TextInput(attrs=attrs),
            widgets.Select(attrs=attrs, choices=Event.DURATION_MULTIPLIER),
        )
        super(UnitsAndDurationWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            if value >= 60:
                return ['{0:g}'.format(float(value) / 60), 60]
            return [int(value), 1]
        return [None, None]


class HTML5EmailInput(widgets.TextInput):
    input_type = 'email'

class HTML5NumberInput(widgets.TextInput):
    input_type = 'number'

class HTML5TelephoneInput(widgets.TextInput):
    input_type = 'tel'

class HTML5DateInput(widgets.DateInput):
    input_type = 'date'

class HTML5DateTimeInput(widgets.DateTimeInput):
    input_type = 'datetime'

class HTML5TimeInput(widgets.TimeInput):
    input_type = 'time'
    
    
class VolunteerCountWidget(HTML5NumberInput):
    
    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        attrs['min'] = 1
        attrs['max'] = 1000
        attrs['size'] = 3
        attrs['style'] = "margin: 0 1ex; text-align: center;"
        return super(VolunteerCountWidget, self).render(name, value, attrs)