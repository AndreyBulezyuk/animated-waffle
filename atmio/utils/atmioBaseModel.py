# component/models.py
from django.db import models


class AtmioBaseModel(models.Model):
    """
    AtmioBaseModel is used for commong fields, properties and Meta
    that is to be applied and used by all models
    """

    metadata = models.JSONField(null=True, blank=True)
    changed_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        abstract = True
