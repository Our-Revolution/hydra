from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from time import time
from .serializers import BSDSerializer
import hmac, hashlib, json, requests, urllib, urlparse


class BSDModel(models.Model):

    BSD_API_HOST    = settings.BSD_API_HOST
    BSD_API_ID      = settings.BSD_API_ID
    BSD_API_SECRET  = settings.BSD_API_SECRET

    FORBIDDEN_FIELDS = []

    class Meta:
        abstract = True

    def get_api_data(self, *args, **kwargs):
        serializer = BSDSerializer()
        return serializer.serialize(self)

    def save(self, *args, **kwargs):
        data = self.get_api_data()
        print data
        req = self._submit(self.get_api_endpoint(), data)
        
        # todo: others, and may vary by model.
        if req.status_code == 200:
            response = json.loads(req.text)
            if 'validation_errors' in response:
                print response
                errors = {}
                for field, error_list in response['validation_errors'].iteritems():
                    errors[field] = ValidationError("%s %s" % (", ".join(errors).title(), field))
                raise ValidationError(errors)
            else:
                return self
        else:
            print req.text
            # raise FieldError()


    def _submit(self, endpoint, data={}, method_name='POST', base="/page/api"):

        timestamp = str(int(time()))

        api_params = data

        api_params.setdefault('api_ver', 2)                 # todo: might be a nice to make an env variable
        api_params.setdefault('api_id', self.BSD_API_ID)
        api_params.setdefault('api_ts', timestamp)

        api_params = sorted(api_params.items())
        api_params.append(('api_mac', hmac.new(self.BSD_API_SECRET.encode(), \
                                        "\n".join([self.BSD_API_ID, \
                                                    timestamp, \
                                                    base + endpoint, \
                                                    '&'.join(["%s=%s" % (k, v) for k, v in api_params])]).encode(), \
                                        hashlib.sha1).hexdigest()))

        url = urlparse.urlunparse(['https', self.BSD_API_HOST, base + endpoint, '', urllib.urlencode(api_params), ''])

        method = getattr(requests, method_name.lower())
        
        # this is naive and will need some more attention probably
        if method_name.lower() == 'get':
            return requests.get(url)
        else:
            return requests.post(url, {'event_api_version': '2', 'values': json.dumps(data, cls=DjangoJSONEncoder)})
