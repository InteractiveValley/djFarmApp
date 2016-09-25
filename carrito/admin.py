# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Sale, DetailSale, ImageSale, Receipt


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'scheduled_order', 'delivered', 'created', 'subtotal', 'discount',
                    'discount_inapam', 'shipping', 'tax', 'total')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('created',)


admin.site.register(Sale, SaleAdmin)


class DetailSaleAdmin(admin.ModelAdmin):
    list_display = (
        'sale', 'sale_date', 'quantity', 'product', 'product_cb', 'price', 'subtotal', 'discount', 'discount_inapam',
        'total', 'need_validation')
    search_fields = (
    'sale__user__email', 'sale__user__first_name', 'sale__user__last_name', 'sale__created', 'product__cb')
    ordering = ('sale', 'id',)


admin.site.register(DetailSale, DetailSaleAdmin)


class ImageSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'image_recipe', 'type_recipe', 'user', 'created', 'modified')
    search_fields = ('sale__user__email', 'sale__user__first_name', 'sale__user__last_name')
    ordering = ('sale', 'id',)


admin.site.register(ImageSale, ImageSaleAdmin)


class ReceiptAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['product', 'quantity', 'status', 'date_expiration']}),
        ('Especiales', {'fields': ['no_lote', 'distribuidor', 'factura']}),

    ]
    list_display = (
        'product', 'user', 'quantity', 'status', 'no_lote', 'distribuidor', 'factura', 'created', 'expiration')
    search_fields = ('product__name', 'product__category__name', 'user__first_name', 'user__last_name',)


admin.site.register(Receipt, ReceiptAdmin)
