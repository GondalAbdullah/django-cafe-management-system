from decimal import Decimal
from django.db import transaction

from .models import Order, OrderItem
from discounts.services import (
    validate_discount,
    calculate_discount_amount,
    apply_discount_atomic,
)
from discounts.models import Discount


def create_order_from_cart(*, user, cart):
    if not cart["items"]:
        raise ValueError("Cart is empty")

    with transaction.atomic():
        total_before = sum(
            Decimal(item["price"]) * item["quantity"]
            for item in cart["items"]
        )

        discount = None
        discount_amount = Decimal("0.00")

        if cart.get("discount_code"):
            discount = Discount.objects.select_for_update().get(
                code=cart["discount_code"]
            )

            validate_discount(
                discount,
                user=user,
                cart_total=total_before,
                cart_items=cart["items"],
            )

            discount_amount = calculate_discount_amount(
                discount,
                cart_total=total_before,
                cart_items=cart["items"],
            )

            apply_discount_atomic(discount, user=user)

        total_after = total_before - discount_amount

        order = Order.objects.create(
            customer=user,
            total_before_discount=total_before,
            discount=discount,
            discount_amount=discount_amount,
            total_after_discount=total_after,
        )

        for item in cart["items"]:
            OrderItem.objects.create(
                order=order,
                menu_item_id=item["menu_item_id"],
                name_snapshot=item["name"],
                price_snapshot=item["price"],
                quantity=item["quantity"],
            )

        return order
