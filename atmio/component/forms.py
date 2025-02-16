from django import forms
from .models import Component
from inventory_level.models import (
    InventoryLevel,
    InventoryLevelMeasurement,
)
from decimal import Decimal


class ComponentForm(forms.ModelForm):
    inventory_level = forms.CharField(
        required=True,
        label="Inventory Level Name",
        # help_text="Enter a name for the inventory level/Sensor/IoT that
        # will be created with this component. This is not the Sensor Value.
    )

    class Meta:
        model = Component
        fields = ["identifier", "description", "inventory_level"]
        read_only_fields = ["created_at", "updated_at"]

    def save(self, commit=True):
        """Override save method to create an associated InventoryLevel"""
        component = super().save(commit=False)

        if commit:
            component.save()

            il = InventoryLevel.objects.create(
                component=component,
                name=self.cleaned_data["inventory_level"],
            )

            InventoryLevelMeasurement.objects.create(
                inventory_level=il, level=Decimal("0.00")
            )

        return component
