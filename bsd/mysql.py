from django.db.backends.mysql.base import DatabaseWrapper as BaseMysqlWrapper
from django.db.backends.mysql.features import DatabaseFeatures as BaseDatabaseFeatures
from django.utils.functional import cached_property



class DatabaseFeatures(BaseDatabaseFeatures):

    @cached_property
    def supports_microsecond_precision(self):
        # hack
        return True

    @cached_property
    def is_sql_auto_is_null_enabled(self):
        # hack
        return False


class DatabaseWrapper(BaseMysqlWrapper):

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.features = DatabaseFeatures(self)