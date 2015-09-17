from django.contrib import admin
from .models import DetailSale, Sale


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'approved','scheduled_order','delivered', 'created', 'subtotal', 'discount', 'total')
    search_fields = ( 'user__email', 'user__first_name','user__last_name')
    ordering = ('created',)

admin.site.register(Sale, SaleAdmin)


class DetailSaleAdmin(admin.ModelAdmin):
    list_display = ('sale', 'quantity','product','price', 'subtotal', 'discount', 'total', 'need_validation','validate')
    search_fields = ( 'sale__user__email', 'sale__user__first_name','sale__user__last_name')
    ordering = ('-id',)

admin.site.register(DetailSale, DetailSaleAdmin)
