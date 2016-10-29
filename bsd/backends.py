from .models import Constituent, ConstituentEmail



class BSDAuthenticationBackend(object):
    
    def __getattr__(self, *args, **kwargs):
        print "yo"
        print args
        print kwargs
        return super(BSDAuthenticationBackend, self).__getattr__(*args, **kwargs)
    

    def get_user(self, cons_id):
        return BSDConstituent.objects.get(cons_id=cons_id)

    def authenticate(self, username, password):
        constituent_email = ConstituentEmail.objects.get(email__iexact=username)
        constituent = constituent_email.cons

        if constituent.check_password(password):
            return constituent