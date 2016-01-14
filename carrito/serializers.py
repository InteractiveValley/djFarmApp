# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import Sale, DetailSale, ImageSale
from productos.serializers import ProductWithoutDiscountSerializer


class DetailSaleListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        detalles = [DetailSale(**item) for item in validated_data]
        import pdb; pdb.set_trace();
        return DetailSale.objects.bulk_create(detalles)


class DetailSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSale
        fields = ('id', 'sale', 'product', 'price', 'quantity', 'subtotal', 'discount', 'total',)
        read_only_fields = ('price', 'subtotal', 'discount', 'total',)


class DetailSaleWithProductSerializer(serializers.ModelSerializer):
    product = ProductWithoutDiscountSerializer(many=False, read_only=True)

    class Meta:
        model = DetailSale
        fields = ('id', 'sale', 'product', 'price', 'quantity', 'subtotal', 'discount', 'total',)
        read_only_fields = ('price', 'subtotal', 'discount', 'total',)


class SaleSerializer(serializers.ModelSerializer):
    detail_sales = DetailSaleWithProductSerializer(many=True, read_only=True, )

    class Meta:
        model = Sale
        fields = ('id', 'user', 'direction', 'status', 'scheduled_order', 'delivered', 'created', 'modified',
                  'detail_sales', 'subtotal', 'discount', 'total', 'notes',)
        read_only_fields = ('user', 'created', 'modified', 'total',)


class ImageSaleListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        images = [ImageSale(**item) for item in validated_data]
        return ImageSale.objects.bulk_create(images)


class ImageSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSale
        list_serializer_class = ImageSaleListSerializer
        fields = ('id', 'sale', 'image_recipe',)
