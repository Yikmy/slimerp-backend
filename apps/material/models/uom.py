from django.db import models
from kernel.core.models.base import BaseModel

class Uom(BaseModel):
    code = models.CharField(max_length=64, unique=True, help_text="UOM code")
    name = models.CharField(max_length=255, help_text="UOM name")

    class Meta(BaseModel.Meta):
        db_table = "material_uom"

    def __str__(self):
        return self.name

class UomConversion(BaseModel):
    from_uom = models.ForeignKey(Uom, on_delete=models.CASCADE, related_name='conversions_from')
    to_uom = models.ForeignKey(Uom, on_delete=models.CASCADE, related_name='conversions_to')
    factor = models.DecimalField(max_digits=18, decimal_places=6, help_text="Conversion factor: 1 from_uom = factor * to_uom")

    class Meta(BaseModel.Meta):
        db_table = "material_uom_conversion"
        unique_together = ('from_uom', 'to_uom')

    def __str__(self):
        return f"1 {self.from_uom.code} = {self.factor} {self.to_uom.code}"
