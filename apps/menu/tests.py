from django.test import TestCase
from django.urls import reverse
from .models import MenuItem

class MenuTests(TestCase):

    def setUp(self):
        MenuItem.objects.create(
            name="Latte",
            description="A classic coffee",
            price=4.50,
            category="Coffee",
            is_active=True,
        )

        MenuItem.objects.create(
            name="Muffin",
            price=2.50,
            category="Pastry",
            is_active=True,
        )

    def test_menu_list_loads(self):
        resp = self.client.get(reverse("menu:list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Latte")
        self.assertContains(resp, "Muffin")

    def test_category_filtering(self):
        resp = self.client.get(reverse("menu:list") + "?category=Coffee")
        self.assertContains(resp, "Latte")
        self.assertNotContains(resp, "Muffin")

    def test_detail_page(self):
        latte = MenuItem.objects.get(name="Latte")
        resp = self.client.get(reverse("menu:detail", args=[latte.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Latte")
