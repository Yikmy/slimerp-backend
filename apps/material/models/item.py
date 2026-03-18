from django.db import models
from kernel.core.models.base import BaseModel
from .category import Category
from .uom import Uom

class Item(BaseModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'

    code = models.CharField(max_length=64, unique=True, help_text="Item code/SKU")
    name = models.CharField(max_length=255, help_text="Item name")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='items')
    base_uom = models.ForeignKey(Uom, on_delete=models.PROTECT, related_name='items')
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.DRAFT)
    spec = models.TextField(blank=True, help_text="Specification")

    class Meta(BaseModel.Meta):
        db_table = "material_item"

    def __str__(self):
        return f"[{self.code}] {self.name}"
