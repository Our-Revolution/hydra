from .auth import Constituent
from .models import ConstituentEmail



class BSDAuthenticationBackend(object):

    def get_user(self, cons_id):
        return Constituent.objects.get(cons_id=cons_id)

    def authenticate(self, username, password):
        
        if not '@' in username:
            return None
        
        try:
            constituent_email = ConstituentEmail.objects.get(email__iexact=username)
            constituent = constituent_email.cons

            if constituent.check_password(password):
                return constituent
        except ConstituentEmail.DoesNotExist:
            pass