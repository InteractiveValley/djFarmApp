# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import Sale, DetailSale, ImageSale
from productos.serializers import ProductWithoutDiscountSerializer


class DetailSaleListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        detalles = [DetailSale(**item) for item in validated_data]
        return DetailSale.objects.bulk_create(detalles)


class DetailSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSale
        fields = ('id', 'sale', 'product', 'price', 'quantity', 'subtotal', 'discount', 'discount_inapam', 'tax',
                  'total')
        read_only_fields = ('price', 'subtotal', 'discount', 'discount_inapam', 'tax', 'total',)


class DetailSaleWithProductSerializer(serializers.ModelSerializer):
    product = ProductWithoutDiscountSerializer(many=False, read_only=True)

    class Meta:
        model = DetailSale
        fields = ('id', 'sale', 'product', 'price', 'quantity', 'subtotal', 'discount', 'discount_inapam', 'tax',
                  'total')
        read_only_fields = ('price', 'subtotal', 'discount', 'discount_inapam', 'tax', 'total',)


class SaleSerializer(serializers.ModelSerializer):
    detail_sales = DetailSaleWithProductSerializer(many=True, read_only=True, )
    status_string = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ('id', 'user', 'direction', 'status', 'scheduled_order', 'delivered', 'created', 'modified',
                  'detail_sales', 'subtotal', 'discount', 'discount_inapam', 'shipping', 'tax', 'total', 'notes',
                  'card_conekta', 'status_string')
        read_only_fields = ('user', 'created', 'modified', 'shipping', 'total',)

    def get_status_string(self, obj):
        return obj.show_status()


class ImageSaleListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        images = [ImageSale(**item) for item in validated_data]
        return ImageSale.objects.bulk_create(images)


class ImageSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSale
        list_serializer_class = ImageSaleListSerializer
        fields = ('id', 'sale', 'image_recipe',)
