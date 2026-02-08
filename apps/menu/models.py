from django.db import models
from django.utils import timezone
from decimal import Decimal

# Create your models here.


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Coffee', 'Coffee'),
        ('Tea', 'Tea'),
        ('Desserts', 'Desserts'),
        ('Savory Snacks', 'Savory Snacks'),
        ('Coffee Beans', 'Coffee Beans'),
        ('Merchandise', 'Merchandise')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)


    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]


    def __str__(self):
        return f"{self.name} ({self.category})"
    

    @property
    def formatted_price(self):
        """For clean display in templates."""
        return f"${self.price:.2f}"