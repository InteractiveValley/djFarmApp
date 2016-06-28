# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import Category, Product, Discount, Laboratory
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='image_category', read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'position', 'image',)


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = ('id', 'name',)


class DiscountSerializer(serializers.ModelSerializer):
    active_discount = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ('id', 'name', 'short_name', 'type', 'price', 'percentage', 'quantity', 'date_begins', 'date_ends',
                  'active_discount')

    def get_active_discount(self, obj):
        now =  timezone.localtime(timezone.now()).date()
        return (obj.date_begins <= now and obj.date_ends >= now)


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='product_image', read_only=True)
    discount = DiscountSerializer()
    category = CategorySerializer()
    laboratory = LaboratorySerializer()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'substances', 'description', 'price', 'with_tax', 'recipe', 'active', 'category',
            'laboratory',
            'image', 'discount', 'inventory','is_antibiotico')


class ProductWithoutDiscountSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='product_image', read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'substances', 'description', 'price', 'recipe', 'active', 'category', 'image',
                  'inventory',)
