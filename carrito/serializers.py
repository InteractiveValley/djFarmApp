from rest_framework import serializers
from .models import Sale, DetailSale, ImageSale


class DetailSaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetailSale
        fields = ('id', 'sale', 'product', 'price', 'quantity', 'subtotal','discount','total', )
        read_only_fields = ('price', 'subtotal', 'discount', 'total', )


class SaleSerializer(serializers.ModelSerializer):

    detail_sales = DetailSaleSerializer(many= True, read_only= True, )

    class Meta:
        model = Sale
        fields = ('id', 'user', 'direction', 'status', 'scheduled_order', 'delivered', 'created', 'modified',
                  'detail_sales','subtotal' ,'discount', 'total', )
        read_only_fields = ('user', 'created', 'modified', 'total',)


class ImageSaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageSale
        fields = ('id', 'sale', 'image_recipe',)