from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from .models import Discount, CustomerDiscountUsage


class DiscountValidationError(Exception):
    pass


def validate_discount(discount, *, user, cart_total, cart_items):
    now = timezone.now()

    if not discount.is_active:
        raise DiscountValidationError("Discount is inactive")

    if not (discount.valid_from <= now <= discount.valid_to):
        raise DiscountValidationError("Discount is expired or not yet active")

    if discount.min_order_value and cart_total < discount.min_order_value:
        raise DiscountValidationError("Order value too low")

    if discount.max_uses is not None and discount.uses_count >= discount.max_uses:
        raise DiscountValidationError("Discount usage limit reached")

    if discount.max_uses_per_customer is not None:
        usage = CustomerDiscountUsage.objects.filter(
            user=user, discount=discount
        ).first()
        if usage and usage.uses >= discount.max_uses_per_customer:
            raise DiscountValidationError("You have already used this discount")

    if discount.type == Discount.ITEM_SPECIFIC:
        item_ids = {item["menu_item_id"] for item in cart_items}
        allowed_ids = set(
            discount.specific_items.values_list("id", flat=True)
        )
        if not item_ids & allowed_ids:
            raise DiscountValidationError(
                "Discount does not apply to items in cart"
            )


def calculate_discount_amount(discount, *, cart_total, cart_items):
    if discount.type == Discount.PERCENTAGE:
        return (cart_total * discount.value / Decimal("100")).quantize(Decimal("0.01"))

    if discount.type == Discount.FIXED:
        return min(discount.value, cart_total)

    if discount.type == Discount.ITEM_SPECIFIC:
        total = Decimal("0.00")
        allowed_ids = set(
            discount.specific_items.values_list("id", flat=True)
        )
        for item in cart_items:
            if item["menu_item_id"] in allowed_ids:
                total += (
                    item["price"]
                    * item["quantity"]
                    * discount.value
                    / Decimal("100")
                )
        return total.quantize(Decimal("0.01"))

    return Decimal("0.00")


def apply_discount_atomic(discount, *, user):
    with transaction.atomic():
        discount = Discount.objects.select_for_update().get(pk=discount.pk)

        if discount.max_uses is not None:
            discount.uses_count += 1
            discount.save(update_fields=["uses_count"])

        if discount.max_uses_per_customer is not None:
            usage, _ = CustomerDiscountUsage.objects.get_or_create(
                user=user, discount=discount
            )
            usage.uses += 1
            usage.save(update_fields=["uses"])
