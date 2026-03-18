from rest_framework import serializers
from apps.material.models import Item, Category, Uom, UomConversion, Barcode, Price

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'code', 'name', 'parent', 'created_at', 'updated_at']

class UomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uom
        fields = ['id', 'code', 'name', 'created_at', 'updated_at']

class UomConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UomConversion
        fields = ['id', 'from_uom', 'to_uom', 'factor', 'created_at', 'updated_at']

class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = ['id', 'barcode', 'item', 'uom', 'created_at', 'updated_at']

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'item', 'price_type', 'currency', 'amount', 'valid_from', 'valid_to', 'created_at', 'updated_at']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'code', 'name', 'category', 'base_uom', 'status', 'spec', 'created_at', 'updated_at']

class ItemDetailSerializer(ItemSerializer):
    barcodes = BarcodeSerializer(many=True, read_only=True)
    prices = PriceSerializer(many=True, read_only=True)
    
    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + ['barcodes', 'prices']
