from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Component
from inventory_level.models import InventoryLevel


class InventoryLevelInline(admin.TabularInline):
    model = InventoryLevel
    extra = 1  # Show 1 empty row for quick addition


@admin.register(Component)
class ComponentAdmin(SimpleHistoryAdmin):  # Use SimpleHistoryAdmin
    list_display = ("identifier", "description", "created_at", "changed_by")
    search_fields = ("identifier", "description")
    ordering = ("-created_at",)
    inlines = [InventoryLevelInline]  # Show related Inventory Levels inline
