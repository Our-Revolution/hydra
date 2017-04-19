from django.db import models, router
from django.core.exceptions import ValidationError



class CrossDatabaseForeignKey(models.ForeignKey):

    def validate(self, value, model_instance):
        if self.remote_field.parent_link:
            return
        super(models.ForeignKey, self).validate(value, model_instance)
        if value is None:
            return

        using = router.db_for_read(self.rel.to, instance=model_instance)
        qs = self.remote_field.model._default_manager.using(using).filter(
            **{self.remote_field.field_name: value}
        )
        qs = qs.complex_filter(self.get_limit_choices_to())
        if not qs.exists():
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={
                    'model': self.remote_field.model._meta.verbose_name, 'pk': value,
                    'field': self.remote_field.field_name, 'value': value,
                },  # 'pk' is included for backwards compatibility
            )