from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import viewsets

class CategoryViewSet(viewsets.ModelViewSet):
	
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
	
    serializer_class = ProductSerializer
    queryset = Product.objects.all()