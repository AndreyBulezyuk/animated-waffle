from django.urls import path
from .views import ComponentListView, ComponentCreateView

urlpatterns = [
    path("components/", ComponentListView.as_view(), name="component-list"),
    path("components/create/", ComponentCreateView.as_view(), name="component-create"),
]
