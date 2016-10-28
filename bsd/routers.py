from django.conf import settings
 
 
class BSDRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "bsd":
            return 'BSD'
        return 'default'
 
    def db_for_write(self, model, **hints):
        if model._meta.app_label == "bsd":
            return 'BSD'
        return 'default'
 
    def allow_relation(self, obj1, obj2, **hints):
        if obj1 and obj2:
            if obj1._meta.app_label == "bsd" or obj2._meta.app_label == "bsd":
                return True
            else:
                return False
        return None
 
    def allow_syncdb(self, db, model):
        """Make sure that apps only appear in the related database."""
        if model._meta.app_label == "bsd":
            return False
        return None
