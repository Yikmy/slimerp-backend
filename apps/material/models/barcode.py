from django.db import models
from kernel.core.models.base import BaseModel
from .item import Item
from .uom import Uom

class Barcode(BaseModel):
    barcode = models.CharField(max_length=128, unique=True, help_text="Barcode string")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='barcodes')
    uom = models.ForeignKey(Uom, on_delete=models.CASCADE, related_name='barcodes')

    class Meta(BaseModel.Meta):
        db_table = "material_barcode"

    def __str__(self):
        return self.barcode
