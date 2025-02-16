import django_filters
from django.db.models import Subquery, OuterRef, FloatField, Min
from django.db.models.functions import Coalesce
from django.db.models import Count
from inventory_level.models import *
from django.db.models import Q
from .models import Component
from django.db.models.query import QuerySet
import django_filters
import logging

logger = logging.getLogger(__name__)


import django_filters
from .models import Component


class ComponentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_search", label="Search")

    order_by = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("created_at", "created_at"),
            ("identifier", "identifier"),
            ("inventory_level", "inventory_level"),
        )
    )

    class Meta:
        model = Component
        fields = ["created_at"]

    def filter_by_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(identifier__startswith=value)

    def filter_by_level(self, value):
        queryset = Component.objects.annotate(
            inventory_level=Min("inventory_levels__last_level")
        ).order_by(value)
        return queryset

    def filter_queryset(self, queryset):
        """ """
        for name, value in self.form.cleaned_data.items():
            if (
                name == "order_by"
                and value is not None
                and ("-inventory_level" in value or "inventory_level" in value)
            ):
                queryset = self.filter_by_level(value[0])
                return queryset
            queryset = self.filters[name].filter(queryset, value)

        return queryset
