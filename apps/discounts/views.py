from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .selectors import get_discount_by_code
from .services import (
    validate_discount,
    calculate_discount_amount,
    DiscountValidationError,
)


@login_required
@require_POST
def apply_discount_view(request):
    code = request.POST.get("code")
    cart = request.session.get("cart")

    if not cart:
        return JsonResponse({"error": "Cart is empty"}, status=400)

    discount = get_discount_by_code(code)
    if not discount:
        return JsonResponse({"error": "Invalid discount code"}, status=404)

    try:
        validate_discount(
            discount,
            user=request.user,
            cart_total=cart["total"],
            cart_items=cart["items"],
        )
        amount = calculate_discount_amount(
            discount,
            cart_total=cart["total"],
            cart_items=cart["items"],
        )
    except DiscountValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "discount_code": discount.code,
        "discount_amount": str(amount),
        "total_after_discount": str(cart["total"] - amount),
    })
