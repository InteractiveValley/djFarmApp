from rest_framework import serializers

from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id','name','image_require','image_no_require')

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('id','name','description','price','require_prescription','is_active','category')