from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from .models import Order
from .services import create_order_from_cart


@login_required
def cart_view(request):
    cart = Cart(request)
    return render(request, "orders/cart.html", {
        "cart": cart.cart,
        "total": cart.get_total(),
        "total_after": cart.get_total_after_discount(),
    })


@require_POST
@login_required
def add_to_cart(request):
    cart = Cart(request)
    cart.add(
        menu_item_id=int(request.POST["menu_item_id"]),
        quantity=int(request.POST.get("quantity", 1)),
    )
    return redirect("orders:cart")


@require_POST
@login_required
def remove_from_cart(request):
    cart = Cart(request)
    cart.remove(int(request.POST["menu_item_id"]))
    return redirect("orders:cart")


@login_required
def checkout_view(request):
    cart = Cart(request)

    if request.method == "POST":
        order = create_order_from_cart(
            user=request.user,
            cart=cart.cart,
        )
        cart.clear()
        return redirect("orders:detail", order.id)

    return render(request, "orders/checkout.html", {
        "cart": cart.cart,
        "total": cart.get_total(),
        "total_after": cart.get_total_after_discount(),
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, "orders/history.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user,
    )
    return render(request, "orders/detail.html", {"order": order})
