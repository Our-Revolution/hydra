from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import SlackInviteForm
import requests



class SlackInviteFormView(FormView):
    form_class = SlackInviteForm
    template_name = 'slack_invite.html'
    success_url = '/join-us-on-slack'

    def form_valid(self, form):
        for slack in form.cleaned_data['slack']:
            req = requests.post('https://%(subdomain)s.slack.com/api/users.admin.invite?email=%(email)s&token=%(api_key)s&set_active=true' % {
                    'subdomain': slack.subdomain,
                    'api_key': slack.api_key,
                    'email': form.cleaned_data['email']
                })

            response_json = req.json()

            if not response_json['ok']:
                if response_json['error'] == 'invalid_email':
                    form.add_error('email', "Invalid email, please try again")
                elif response_json['error'] == 'invalid_auth':
                    # bad token! let them know but email for help.
                    from django.core.mail import mail_admins
                    mail_admins('Bad Slack Token for %s (EOM)' % slack.name, '')
                    form.add_error('slack', "Hmm something is wrong with the Slack configuration for %s our end. We'll take a look ASAP, sorry about that!" % slack.name)
                elif response_json['error'] == 'already_invited':
                    form.add_error('slack', "Looks like you've already been invited to %s!" % slack.name)
                    

        if form.errors:
            return super(SlackInviteFormView, self).form_invalid(form)

        messages.success(self.request, "Success! You've been invited to %s Slack groups." % form.cleaned_data['slack'].count())
        return super(SlackInviteFormView, self).form_valid(form)
