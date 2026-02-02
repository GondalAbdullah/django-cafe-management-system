from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from menu.models import MenuItem
from .services import create_order_from_cart

User = get_user_model()


class OrderCreationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com", password="123456"
        )
        self.item = MenuItem.objects.create(
            name="Latte",
            price=Decimal("5.00"),
            category="Coffee",
        )

    def test_order_creation(self):
        cart = {
            "items": [{
                "menu_item_id": self.item.id,
                "name": "Latte",
                "price": Decimal("5.00"),
                "quantity": 2,
            }],
            "discount_code": None,
            "discount_amount": Decimal("0.00"),
        }

        order = create_order_from_cart(
            user=self.user,
            cart=cart,
        )

        self.assertEqual(order.total_before_discount, Decimal("10.00"))
        self.assertEqual(order.items.count(), 1)
