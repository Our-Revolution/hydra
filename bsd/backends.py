from .models import Constituent



class BSDAuthenticationBackend(object):

    def get_user(self, cons_id):
        return BSDConstituent.objects.get(cons_id=cons_id)

    def authenticate(self, email, password):
        constituent_email = ConstituentEmail.objects.get(email__iexact=email)
        constituent = constituent_email.Constituent

        if constituent.check_password(password):
            return constituent