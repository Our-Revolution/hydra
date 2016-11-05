from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from bsd.auth import Constituent
from .forms import BlastEmailForm

import csv, requests


class IndexView(TemplateView):
    template_name = 'splash.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, Constituent):
            return redirect('events-list')
        return super(IndexView, self).get(request, *args, **kwargs)



class BlastEmail(FormView):
    form_class = BlastEmailForm
    template_name = "admin/blast_email_form.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(BlastEmail, self).get_context_data(*args, **kwargs)
        context_data['title'] = "Blast Email"
        context_data['has_permission'] = True
        return context_data

    def get_initial(self):
        return {
            'sender_name': "Our Revolution", # self.request.user,
            'sender_email': "organizing@ourrevolution.com",
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

        print recipients
        print recipient_variables

    # def form_invalid(self, form):
    #     import ipdb; ipdb.set_trace()