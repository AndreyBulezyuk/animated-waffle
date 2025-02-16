import logging
from django.apps import AppConfig

logger = logging.getLogger("inventory_level")


class InventoryLevelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory_level"

    def ready(self):
        logger.debug("📢 InventoryLevelConfig: Signals are being loaded.")
        import inventory_level.signals  # ✅ Ensure signals are connected
