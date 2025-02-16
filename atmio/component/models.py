# component/models.py
from django.db import models
from simple_history.models import HistoricalRecords
from utils.atmioBaseModel import AtmioBaseModel


class Component(AtmioBaseModel):
    """A Component is defined by a customer-given identifier and a description."""

    identifier = models.CharField(
        max_length=30, unique=True, blank=False, null=False, default="1"
    )
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]
        # Since End-User will probably search by identifier, we should index it
        # to improve performance.
        indexes = [models.Index(fields=["identifier"])]

    def __str__(self):
        return self.identifier
