from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import InventoryLevel, InventoryLevelMeasurement


class InventoryLevelMeasurementInline(admin.TabularInline):
    model = InventoryLevelMeasurement
    extra = 2  # Show 2 empty rows for quick addition


@admin.register(InventoryLevel)
class InventoryLevelAdmin(SimpleHistoryAdmin):  # Use SimpleHistoryAdmin
    list_display = ("name", "last_level", "component", "metadata_display")
    search_fields = ("name", "component__identifier")
    ordering = ("name",)
    list_filter = ("component",)
    inlines = [InventoryLevelMeasurementInline]  # Show related Measurements inline

    def metadata_display(self, obj):
        return obj.metadata if obj.metadata else "N/A"

    metadata_display.short_description = "Metadata"


@admin.register(InventoryLevelMeasurement)
class InventoryLevelMeasurementAdmin(admin.ModelAdmin):
    list_display = ("inventory_level", "level", "timestamp", "metadata_display")
    search_fields = ("inventory_level__name",)
    ordering = ("-timestamp",)
    list_filter = ("inventory_level",)

    def metadata_display(self, obj):
        return obj.metadata if obj.metadata else "N/A"

    metadata_display.short_description = "Metadata"
