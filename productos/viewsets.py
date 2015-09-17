from .models import Category, Product, Discount
from .serializers import CategorySerializer, ProductSerializer, DiscountSerializer
from rest_framework import viewsets
from rest_framework import filters


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = ( filters.DjangoFilterBackend, )
    filter_fields = ('category', 'name', )


class DiscountViewSet(viewsets.ModelViewSet):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()