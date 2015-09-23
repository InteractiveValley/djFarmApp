from rest_framework import serializers
from .models import Category, Product, Discount


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'image_require', 'image_no_require')


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = ('id', 'name', 'short_name', 'type', 'price', 'percentage', 'quantity', 'date_begins', 'date_ends',)


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='product_image', read_only=True)
    discount = DiscountSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'require_prescription', 'active', 'category',
                  'image', 'discount',)
