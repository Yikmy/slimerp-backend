from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemViewSet, CategoryViewSet, UomViewSet,
    UomConversionViewSet, BarcodeViewSet, PriceViewSet
)

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'uoms', UomViewSet, basename='uom')
router.register(r'conversions', UomConversionViewSet, basename='conversion')
router.register(r'barcodes', BarcodeViewSet, basename='barcode')
router.register(r'prices', PriceViewSet, basename='price')

urlpatterns = [
    path('', include(router.urls)),
]