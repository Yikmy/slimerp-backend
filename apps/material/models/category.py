from django.db import models
from kernel.core.models.base import BaseModel

class Category(BaseModel):
    code = models.CharField(max_length=64, unique=True, help_text="Category code")
    name = models.CharField(max_length=255, help_text="Category name")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', help_text="Parent category")

    class Meta(BaseModel.Meta):
        db_table = "material_category"

    def __str__(self):
        return f"[{self.code}] {self.name}"
