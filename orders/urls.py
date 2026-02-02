from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/", views.add_to_cart, name="add"),
    path("cart/remove/", views.remove_from_cart, name="remove"),
    path("checkout/", views.checkout_view, name="checkout"),

    path("", views.order_history, name="history"),
    path("<int:order_id>/", views.order_detail, name="detail"),
]
