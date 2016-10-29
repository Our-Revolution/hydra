from django.forms import widgets
from .models import Event



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