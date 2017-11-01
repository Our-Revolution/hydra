from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.gis.geos import Point, GEOSGeometry
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from bsd.auth import Constituent
from bsd.decorators import class_view_decorator
from bsd.models import ConstituentAddress
from .forms import BlastEmailForm, GeoTargetForm
import csv, json, requests
import logging

logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = 'splash.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, Constituent):
            return redirect('events-list')
        return super(IndexView, self).get(request, *args, **kwargs)

@class_view_decorator(staff_member_required)
class GeoTarget(FormView):
    form_class = GeoTargetForm
    template_name = "admin/geo_target_form.html"
    success_url = "admin/geo-target"

    def form_invalid(self, form):
        response = super(GeoTarget, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors.as_json(), safe=False, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(GeoTarget, self).form_valid(form)
        if self.request.is_ajax():

            cons_ids = []
            kwargs = {'state_cd': form.cleaned_data['state']}

            if form.cleaned_data['primary_only']:
                kwargs['is_primary'] = True

            # Get all constituent addresses in the state
            cons_addrs = ConstituentAddress.objects.filter(**kwargs)

            geojson = json.loads(form.cleaned_data['geojson'])

            if geojson['type'] == 'FeatureCollection':
                # todo: fetch number, but stick to 1st for now
                logger.debug('is FeatureCollection')
                geojson = geojson['features'][0]['geometry']

            # elif geojson['type'] not ['MultiPolygon', 'Polygon']:

            poly = GEOSGeometry(json.dumps(geojson))

            for con in cons_addrs:
               point = Point(y=con.latitude, x=con.longitude)
               if poly.contains(point):
                  cons_ids.append(con.cons_id)

            return JsonResponse(cons_ids, safe=False)
        else:
            return response



@class_view_decorator(staff_member_required)
class BlastEmail(FormView):
    form_class = BlastEmailForm
    template_name = "admin/blast_email_form.html"
    success_url = "/admin/blast-email"

    def get_context_data(self, *args, **kwargs):
        context_data = super(BlastEmail, self).get_context_data(*args, **kwargs)
        context_data['title'] = "Blast Email"
        context_data['has_permission'] = True
        return context_data

    def get_initial(self):
        return {
            'sender_name': "Our Revolution", # self.request.user,
            'sender_email': "info@ourrevolution.com",
            'message': """



----
Paid for by Our Revolution
(not the billionaires)

603 2ND STREET NE - WASHINGTON, DC 20002

Email is one of the most important tools we have to reach supporters like you, but if you'd like to, click here to unsubscribe: https://go.ourrevolution.com/page/unsubscribe/"""
        }

    def form_valid(self, form):
        file = self.request.FILES['recipients_csv'].file
        reader = csv.DictReader(file)
        email_addresses = [row[self.request.POST['email_field']] for row in reader]
        recipients = ", ".join(email_addresses)
        recipient_variables = dict((email, {}) for email in email_addresses)

        MAX = 1000

        # print len(email_addresses)

        if len(email_addresses) > MAX:

            page = 0

            while True:

                email_addresses_batch = email_addresses[page*MAX:(page+1)*MAX]
                recipient_variables_batch = dict((email, {}) for email in email_addresses_batch)

                # print page*MAX

                # print "Sending page %s to:" % page
                # print email_addresses_batch

                post = requests.post("https://api.mailgun.net/v3/%s/messages" % settings.MAILGUN_SERVER_NAME,
                                auth=("api", settings.MAILGUN_ACCESS_KEY),
                                data={"from": "%s <%s>" % (self.request.POST['sender_display_name'], self.request.POST['sender_email']),
                                          "to": [", ".join(email_addresses_batch)],
                                          "subject": self.request.POST['subject'],
                                          "text": self.request.POST['message'],
                                          "recipient-variables": (json.dumps(recipient_variables_batch))
                                    })

                if post.status_code != 200:
                    raise ValueError(json.loads(post.text)['message'])

                page += 1

                if page * MAX >= len(email_addresses):
                    break

        else:

            post = requests.post("https://api.mailgun.net/v3/%s/messages" % settings.MAILGUN_SERVER_NAME,
                            auth=("api", settings.MAILGUN_ACCESS_KEY),
                            data={"from": "%s <%s>" % (self.request.POST['sender_display_name'], self.request.POST['sender_email']),
                                      "to": [", ".join(email_addresses)],
                                      "subject": self.request.POST['subject'],
                                      "text": self.request.POST['message'],
                                      "recipient-variables": (json.dumps(recipient_variables))
                                })

            if post.status_code != 200:
                raise ValueError(json.loads(post.text)['message'])

        # success / error handle
        messages.success(self.request, "Sent %s to %s recipients." % (self.request.POST['subject'], len(email_addresses)))

        return super(BlastEmail, self).form_valid(form)

    # def form_invalid(self, form):
    #     import ipdb; ipdb.set_trace()
