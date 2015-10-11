from rest_framework import serializers
from .models import Category, Product, Discount


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', )


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
        fields = ('id', 'name', 'substances', 'description', 'price', 'recipe', 'active', 'category', 'image',
                  'discount','inventory')


class ProductWithoutDiscountSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='product_image', read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'substances', 'description', 'price', 'recipe', 'active', 'category', 'image',
                  'inventory')
