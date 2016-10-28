import json
from django.db import models
from django.utils import six
from django.utils.encoding import force_text, is_protected_type




class BSDSerializer(object):

    def serialize(self, obj, **options):
    
        self.object = {}
        
        concrete_model = obj._meta.concrete_model
        for field in concrete_model._meta.local_fields:

            if field.name in obj.FORBIDDEN_FIELDS:
                continue
                
            if field.remote_field is None:
                self.handle_field(obj, field)

            else:
                self.handle_fk_field(obj, field)

        return self.object

        
    def handle_field(self, obj, field):
        value = field.value_from_object(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if is_protected_type(value):
            self.object[field.name] = value
        else:
            self.object[field.name] = field.value_to_string(obj)
            
            
    def handle_fk_field(self, obj, field):
        self.object["%s_id" % field.name] = getattr(obj, "%s_id" % field.name)