from decimal import Decimal
from menu.models import MenuItem


class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(self.SESSION_KEY)

        if not self.cart:
            self.cart = {
                "items": [],
                "discount_code": None,
                "discount_amount": Decimal("0.00"),
            }
            self.session[self.SESSION_KEY] = self.cart

    def save(self):
        self.session.modified = True

    def add(self, menu_item_id, quantity=1):
        menu_item = MenuItem.objects.get(pk=menu_item_id)

        for item in self.cart["items"]:
            if item["menu_item_id"] == menu_item_id:
                item["quantity"] += quantity
                self.save()
                return

        self.cart["items"].append({
            "menu_item_id": menu_item.id,
            "name": menu_item.name,
            "price": menu_item.price,
            "quantity": quantity,
        })
        self.save()

    def remove(self, menu_item_id):
        self.cart["items"] = [
            i for i in self.cart["items"]
            if i["menu_item_id"] != menu_item_id
        ]
        self.clear_discount()
        self.save()

    def clear(self):
        self.session.pop(self.SESSION_KEY, None)
        self.save()

    def clear_discount(self):
        self.cart["discount_code"] = None
        self.cart["discount_amount"] = Decimal("0.00")

    def get_total(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart["items"]
        )

    def get_total_after_discount(self):
        return self.get_total() - Decimal(self.cart["discount_amount"])
