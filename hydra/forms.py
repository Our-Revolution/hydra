from django import forms
from django.contrib import admin
from localflavor.us.forms import USStateSelect
import json


class BlastEmailForm(forms.Form):
    sender_display_name = forms.CharField(max_length=1024, label="Sender Display Name", widget=admin.widgets.AdminTextInputWidget)
    sender_email = forms.EmailField(max_length=1024, label="Sender Email", widget=admin.widgets.AdminTextInputWidget)
    subject = forms.CharField(max_length=1024, widget=admin.widgets.AdminTextInputWidget)
    message = forms.CharField(max_length=4096, widget=admin.widgets.AdminTextareaWidget)
    recipients_csv = forms.FileField(label="Recipients (CSV)")
    email_field = forms.CharField(max_length=128, label="Email Field", help_text="This gets autopopulated after you upload a CSV")


class GeoTargetForm(forms.Form):
    state = forms.CharField(initial="FL", max_length=2, label="State Abbreviation")
    geojson = forms.CharField(max_length=1000000, widget=admin.widgets.AdminTextareaWidget, label="GeoJSON", help_text="You'll need to fetch this from Census.gov or Google or some such; ping Juliana or Jon. :D")
    primary_only = forms.BooleanField(initial=True, label="Primary Addresses Only", help_text="Recommended")

    def clean_geojson(self):
        try:
            json_data = json.loads(self.cleaned_data['geojson'])
        except ValueError:
            raise forms.ValidationError("We don't recognize that GeoJSON, please try again.")

        try:
            if json_data['type'] == "FeatureCollection":
                assert json_data['features'][0]['type'] == 'Feature' and \
                         json_data['features'][0]['geometry']['type'] in ['Polygon', 'MultiPolygon']
            else:
                assert json_data['type'] in ['Polygon', 'MultiPolygon']
        except (IndexError, AssertionError):
            raise forms.ValidationError("We don't recognize that GeoJSON, please try again.")

        return self.cleaned_data['geojson']
