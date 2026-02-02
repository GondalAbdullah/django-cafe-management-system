from django.utils import timezone
from .models import Discount


def get_active_discounts():
    now = timezone.now()
    
    return Discount.objects.filter(
        is_active=True,
        valid_from__lte=now,
        valid_to__gte=now,
    )


def discount_by_code(code):
    return Discount.objects.filter(code__iexact=code).first()