from django.utils import timezone
from kernel.core.db.transaction import atomic, on_commit
from kernel.core.exceptions import BusinessError
from kernel.support.hooks import dispatch_hook
from apps.material.models import Item, Category, Uom, UomConversion, Barcode, Price


@atomic
def create_category(user, **data) -> Category:
    return Category.objects.create(created_by=user, updated_by=user, **data)


@atomic
def create_uom(user, **data) -> Uom:
    return Uom.objects.create(created_by=user, updated_by=user, **data)


@atomic
def create_item(user, **data) -> Item:
    if Item.objects.filter(code=data.get('code')).exists():
        raise BusinessError(code="CONFLICT", message="Item with this code already exists")

    item = Item.objects.create(created_by=user, updated_by=user, **data)

    def trigger_created_hook():
        dispatch_hook('material.item_created', payload={
            'item_id': str(item.id),
            'operator_id': str(user.id) if user else None,
            'timestamp': timezone.now().isoformat()
        })
    on_commit(trigger_created_hook)

    return item


@atomic
def update_item(user, item: Item, **data) -> Item:
    old_status = item.status
    for key, value in data.items():
        setattr(item, key, value)
    item.updated_by = user
    item.save()

    def trigger_updated_hooks():
        payload = {
            'item_id': str(item.id),
            'operator_id': str(user.id) if user else None,
            'timestamp': timezone.now().isoformat()
        }
        dispatch_hook('material.item_updated', payload=payload)

        if old_status != item.status:
            payload['old_status'] = old_status
            payload['new_status'] = item.status
            dispatch_hook('material.item_status_changed', payload=payload)

    on_commit(trigger_updated_hooks)
    return item


@atomic
def delete_item(user, item: Item):
    item.delete()


@atomic
def create_conversion(user, **data) -> UomConversion:
    return UomConversion.objects.create(created_by=user, updated_by=user, **data)


@atomic
def create_barcode(user, **data) -> Barcode:
    return Barcode.objects.create(created_by=user, updated_by=user, **data)


@atomic
def create_price(user, **data) -> Price:
    return Price.objects.create(created_by=user, updated_by=user, **data)
