from django.contrib import admin
from .models import Category, Product, Discount, Laboratory


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Thumbnails', {'fields': ['image_category'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'thumbnail',)
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Laboratory, LaboratoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['name', 'substances', 'category', 'laboratory', 'description', ]}),
        ('Thumbnails', {'fields': ['image_no_require', 'image_require_show', 'image_require'],
                        'classes': ['collapse']}),
        ('Detalle', {'fields': ['price', 'inventory', 'with_tax', 'active', 'recipe', ]}),
        ('Descuento', {'fields': ['discount', ]}),
    ]
    list_display = ('name', 'substances', 'category', 'price', 'with_tax', 'status_inventory', 'active', 'thumbnail',)
    search_fields = ('name', 'category__name', 'substances',)


admin.site.register(Product, ProductAdmin)


class DiscountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['name', 'short_name', 'type', 'price', 'percentage', 'quantity', ]}),
        ('Vigencias', {'fields': ['date_begins', 'date_ends', ]}),
    ]
    list_display = ('name', 'type', 'price', 'percentage', 'quantity', 'date_begins', 'date_ends')
    search_fields = ('name', 'type', 'date_begins', 'date_ends',)


admin.site.register(Discount, DiscountAdmin)
