from rest_framework import viewsets
from rest_framework.request import Request
from kernel.core.api.responses import success_response
from apps.material import selectors, services
from apps.material.models import Category, Uom, UomConversion, Barcode, Price
from .serializers import (
    ItemSerializer, ItemDetailSerializer, CategorySerializer,
    UomSerializer, UomConversionSerializer, BarcodeSerializer, PriceSerializer
)


class BaseResponseViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)  # pyright: ignore[reportUnreachable]
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data={"items": serializer.data, "total": len(serializer.data)})

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return success_response(data={
            "items": data,
            "page": self.paginator.page.number,
            "page_size": self.paginator.page.paginator.per_page,
            "total": self.paginator.page.paginator.count
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data)


class CategoryViewSet(BaseResponseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = services.create_category(request.user, **serializer.validated_data)
        return success_response(data=self.get_serializer(category).data)


class UomViewSet(BaseResponseViewSet):
    queryset = Uom.objects.all()
    serializer_class = UomSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uom = services.create_uom(request.user, **serializer.validated_data)
        return success_response(data=self.get_serializer(uom).data)


class UomConversionViewSet(BaseResponseViewSet):
    queryset = UomConversion.objects.all()
    serializer_class = UomConversionSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversion = services.create_conversion(request.user, **serializer.validated_data)
        return success_response(data=self.get_serializer(conversion).data)


class BarcodeViewSet(BaseResponseViewSet):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        barcode = services.create_barcode(request.user, **serializer.validated_data)
        return success_response(data=self.get_serializer(barcode).data)


class PriceViewSet(BaseResponseViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        price = services.create_price(request.user, **serializer.validated_data)
        return success_response(data=self.get_serializer(price).data)


class ItemViewSet(BaseResponseViewSet):
    def get_queryset(self):
        search = self.request.query_params.get('search')
        category_id = self.request.query_params.get('category_id')
        status = self.request.query_params.get('status')
        return selectors.list_items(search=search, category_id=category_id, status=status)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ItemDetailSerializer
        return ItemSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = services.create_item(request.user, **serializer.validated_data)
        return success_response(data=self.get_serializer(item).data)

    def update(self, request: Request, *args, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        item = services.update_item(request.user, item, **serializer.validated_data)
        return success_response(data=self.get_serializer(item).data)

    def destroy(self, request: Request, *args, **kwargs):
        item = self.get_object()
        services.delete_item(request.user, item)
        return success_response(message="Item deleted")
