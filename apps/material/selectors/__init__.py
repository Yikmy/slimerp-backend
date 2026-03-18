from typing import Optional
from django.db.models import QuerySet, Q
from apps.material.models import Item, Category, Uom, UomConversion, Barcode, Price


def get_item(item_id: str) -> Optional[Item]:
    return Item.objects.filter(id=item_id).first()


def list_items(
    search: Optional[str] = None,
    category_id: Optional[str] = None,
    status: Optional[str] = None
) -> QuerySet[Item]:
    qs = Item.objects.all()

    if search:
        # Search by name, code, or barcode
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(barcodes__barcode__icontains=search)
        ).distinct()

    if category_id:
        qs = qs.filter(category_id=category_id)

    if status:
        qs = qs.filter(status=status)

    return qs


def list_categories() -> QuerySet[Category]:
    return Category.objects.all()


def list_uoms() -> QuerySet[Uom]:
    return Uom.objects.all()


def list_conversions() -> QuerySet[UomConversion]:
    return UomConversion.objects.all()


def list_barcodes() -> QuerySet[Barcode]:
    return Barcode.objects.all()


def list_prices() -> QuerySet[Price]:
    return Price.objects.all()
