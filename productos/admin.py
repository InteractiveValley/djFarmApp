from django.contrib import admin
from .models import Category, Product, Discount


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Thumbnails', {'fields': ['image_require', 'image_no_require'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'require', 'no_require',)
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['name', 'description', 'category']}),
        ('Detalle', {'fields': ['price', 'active', 'require_prescription']}),
    ]
    list_display = ('name', 'category', 'price', 'active', 'require_prescription', 'thumbnail')
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)


class DiscountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['type', 'price', 'percentage','quantity', ]}),
        ('Vigencias', {'fields': ['date_begins', 'date_ends', ]}),
        ('Relaciones', {'fields': ['products', ]}),
    ]
    list_display = ('type', 'price', 'percentage', 'quantity', 'date_begins', 'date_ends')
    search_fields = ('type', 'date_begins', 'date_ends', )


admin.site.register(Discount, DiscountAdmin)