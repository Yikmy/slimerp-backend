from django.db import models
from kernel.core.models.base import BaseModel
from .item import Item

class Price(BaseModel):
    class PriceType(models.TextChoices):
        STANDARD = 'STANDARD', 'Standard Price'
        PROMO = 'PROMO', 'Promotional Price'

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='prices')
    price_type = models.CharField(max_length=32, choices=PriceType.choices, default=PriceType.STANDARD)
    currency = models.CharField(max_length=10, default='USD')
    amount = models.DecimalField(max_digits=18, decimal_places=6)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        db_table = "material_price"

    def __str__(self):
        return f"{self.item.code} - {self.price_type}: {self.amount} {self.currency}"
