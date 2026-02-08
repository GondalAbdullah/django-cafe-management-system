from django.urls import path
from .views import apply_discount_view

app_name = "discounts"

urlpatterns = [
    path("apply/", apply_discount_view, name="apply"),
]
