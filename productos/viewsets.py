# -*- encoding: utf-8 -*-
from .models import Category, Product, Discount
from .serializers import CategorySerializer, ProductSerializer, DiscountSerializer
from rest_framework import viewsets, filters
from django.utils import timezone


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('category', 'name',)
    search_fields = ('name', 'description', 'category__name', 'substances',)


class DiscountViewSet(viewsets.ModelViewSet):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the directions
        for the currently authenticated user.
        """
        now = timezone.now().date()
        return Discount.objects.filter(date_begins__lte=now, date_ends__gte=now)
