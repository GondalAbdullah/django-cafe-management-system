from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Discount(models.Model):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    ITEM_SPECIFIC = "item_specific"

    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, "Percentage"),
        (FIXED, "Fixed Amount"),
        (ITEM_SPECIFIC, "Item Specific"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(max_digits=8, decimal_places=2)

    min_order_value = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    max_uses = models.PositiveIntegerField(null=True, blank=True)
    uses_count = models.PositiveIntegerField(default=0)

    max_uses_per_customer = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    specific_items = models.ManyToManyField(
        "menu.MenuItem", blank=True, related_name="discounts"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["valid_from", "valid_to"]),
        ]

    def clean(self):
        if self.valid_from >= self.valid_to:
            raise ValidationError("valid_from must be before valid_to")

    def __str__(self):
        return f"{self.name} ({self.code})"


class CustomerDiscountUsage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE
    )
    uses = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "discount")

    def __str__(self):
        return f"{self.user} → {self.discount.code} ({self.uses})"
