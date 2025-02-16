import logging
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpRequest, HttpResponse
from django.views import View
from django_filters.views import FilterView
from django.views.generic import ListView
from django.db.models import Min, Max
from django.db.models.query import QuerySet
from .models import Component
from inventory_level.models import InventoryLevel
from .forms import ComponentForm
from .filters import ComponentFilter

logger = logging.getLogger(__name__)


class ComponentListView(FilterView, ListView):
    model = Component
    filterset_class = ComponentFilter
    paginate_by = 10
    template_name = "component/component_list.html"
    context_object_name = "components"

    def get_context_data(self, **kwargs) -> dict:
        """Handles pagination, filters, and context variables."""
        context = super().get_context_data(**kwargs)
        page_obj = context["page_obj"]

        context.update(
            {
                "query_string": self.request.GET.urlencode(),
                "has_next": page_obj.has_next(),
                "next_page_number": (
                    page_obj.next_page_number() if page_obj.has_next() else None
                ),
            }
        )
        return context

    def render_to_response(self, context: dict, **response_kwargs) -> HttpResponse:
        """Return partial template for HTMX requests"""
        if self.request.headers.get("HX-Request") == "true":
            return render(
                self.request, "component/component_list_partial.html", context
            )
        return super().render_to_response(context, **response_kwargs)


class ComponentCreateView(View):
    def get(self, request, *args, **kwargs):
        try:
            form = ComponentForm()
            return render(request, "component/component_form.html", {"form": form})
        except Exception as e:
            logger.exception("Error in ComponentCreateView.get: %s", e)
            return HttpResponseBadRequest("Bad Request")

    def post(self, request, *args, **kwargs):
        try:
            form = ComponentForm(request.POST)
            if form.is_valid():
                component = form.save()
                context = {"component": component}
                response = render(request, "component/component_row.html", context)
                return response
            else:
                return render(request, "component/component_form.html", {"form": form})
        except Exception as e:
            logger.exception("Error in ComponentCreateView.post: %s", e)
            return HttpResponseBadRequest("Bad Request")
