from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("name_snapshot", "price_snapshot", "quantity")
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_after_discount", "status", "order_date")
    list_filter = ("status",)
    inlines = [OrderItemInline]
