from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Discount
from .services import calculate_discount_amount

User = get_user_model()


class DiscountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="a@a.com", password="pass1234"
        )

        self.discount = Discount.objects.create(
            name="Ten Percent",
            code="TEN10",
            type=Discount.PERCENTAGE,
            value=Decimal("10"),
            valid_from=timezone.now() - timezone.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
        )

    def test_percentage_discount(self):
        amount = calculate_discount_amount(
            self.discount,
            cart_total=Decimal("200"),
            cart_items=[],
        )
        self.assertEqual(amount, Decimal("20.00"))
