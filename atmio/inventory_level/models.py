# inventory_level/models.py
from django.db import models
from decimal import Decimal
from component.models import Component
from simple_history.models import HistoricalRecords
from utils.atmioBaseModel import AtmioBaseModel


class InventoryLevel(AtmioBaseModel):
    """Each InventoryLevel belongs to one Component.
    Assuming InventoryLevel ~= Senor/IoT Device that can have multiple Measurements.

    It's unclear if Component <-> InventoryLevel is a one-to-one or one-to-many relationship.
    Assuming it's one-to-many, as a Component can have multiple InventoryLevels.
    """

    component = models.ForeignKey(
        Component, on_delete=models.PROTECT, related_name="inventory_levels"
    )
    # To represent a Tree like Structure of Inventory Levels, i'll add M2M field to self.
    # Additionally i'll add a 'children' field, in order to reduce computation time as trade-off for more storage.
    # Explanation: By adding a 'children' field, we can reduce the computation time to get all children of a node,
    # instead of querying the database for all nodes with parent = node. In theory, the whole
    # "Tree Structure" Information is already present with only 'parents_inventory_level'
    parents_inventory_level = models.ManyToManyField("self", blank=True)
    children_inventory_level = models.ManyToManyField("self", blank=True)

    # Sensor or IoT-device name that measured this level.
    last_level = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    name = models.CharField(max_length=100)
    metadata = models.JSONField(null=True, blank=True)
    # To log who CRUD the InventoryLevel and when.
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class InventoryLevelMeasurement(models.Model):
    """Each InventoryLevelMeasurement belongs to one InventoryLevel."""

    # Assuming that an invetory level will have many measurements (e.g. every hour).
    # Meaning we have to save every measurement in a separate Model.
    # Alternatively, we could save the measurements as a JSONField or make use of the DjangoSimpleHistory plugin.
    # Tradeoff: Django Simple History plugin is easier to implement, but querying the data will be slower + more storage.

    inventory_level = models.ForeignKey(
        InventoryLevel, on_delete=models.CASCADE, related_name="measurements"
    )
    # The level of the inventory at the time of the measurement.
    level = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    # The time at which the measurement was taken.
    timestamp = models.DateTimeField(auto_now_add=True)
    # Metadata for the measurement, e.g. sensor, location, temperature, etc.
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.inventory_level.name} - {self.level} - {self.timestamp}"
