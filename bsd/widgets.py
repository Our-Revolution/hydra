from django.forms import widgets


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