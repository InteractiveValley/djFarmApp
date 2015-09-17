from rest_framework import serializers
from .models import Sale, DetailSale


class DetailSaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetailSale
        fields = ('id', 'sale', 'product', 'price', 'quantity', 'subtotal','discount','total', 'image_recipe', 'validate', )
        read_only_fields = ('price', 'subtotal', 'discount', 'total', )


class SaleSerializer(serializers.ModelSerializer):

    detail_sales = DetailSaleSerializer(many= True, read_only= True, )

    class Meta:
        model = Sale
        fields = ('id', 'user', 'direction', 'approved', 'scheduled_order', 'delivered', 'created', 'modified',
                  'detail_sales','subtotal' ,'discount', 'total', )
        read_only_fields = ('user', 'approved', 'approved', 'scheduled_order', 'delivered', 'created',
                            'modified', 'total',)


