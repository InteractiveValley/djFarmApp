# -*- encoding: utf-8 -*-
from .models import Sale, DetailSale, ImageSale
from .serializers import SaleSerializer, DetailSaleSerializer, ImageSaleSerializer
from rest_framework import viewsets
from rest_framework import filters


class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    filter_backends = ( filters.DjangoFilterBackend, )
    filter_fields = ('id', 'user', )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the directions
        for the currently authenticated user.
        """
        user = self.request.user
        return Sale.objects.filter(user=user)


class DetailSaleViewSet(viewsets.ModelViewSet):
    serializer_class = DetailSaleSerializer
    queryset = DetailSale.objects.all()
    filter_backends = ( filters.DjangoFilterBackend, )
    filter_fields = ('sale', )


class ImageSaleViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSaleSerializer
    queryset = ImageSale.objects.all()
    filter_backends = ( filters.DjangoFilterBackend, )
    filter_fields = ('sale', )