import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InventoryLevelMeasurement, InventoryLevel

logger = logging.getLogger("inventory_level")


@receiver(post_save, sender=InventoryLevelMeasurement)
def update_last_level(sender, instance, **kwargs):
    """
    Ensure `InventoryLevel.last_level` updates whenever a new measurement is created.
    """
    inventory_level = instance.inventory_level

    # ✅ Fetch latest measurement from DB to avoid stale data
    latest_measurement = inventory_level.measurements.order_by("-timestamp").first()
    if latest_measurement:
        inventory_level.last_level = latest_measurement.level
        inventory_level.save(update_fields=["last_level"])

        logger.debug(
            f"📢 Signal Fired: Updated InventoryLevel ID={inventory_level.id} "
            f"from last_level to {inventory_level.last_level}"
        )
    else:
        logger.warning(
            f"⚠️ No measurement found for InventoryLevel ID={inventory_level.id}"
        )
