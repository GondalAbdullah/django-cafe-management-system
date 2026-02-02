from django.contrib import admin
from .models import Discount, CustomerDiscountUsage


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "type",
        "value",
        "is_active",
        "uses_count",
    )
    list_filter = ("type", "is_active")
    search_fields = ("name", "code")
    filter_horizontal = ("specific_items",)


@admin.register(CustomerDiscountUsage)
class CustomerDiscountUsageAdmin(admin.ModelAdmin):
    list_display = ("user", "discount", "uses")
