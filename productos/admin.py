from django.contrib import admin
from .models import Category, Product, Discount


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Thumbnails', {'fields': ['image_no_require', 'image_require_show', 'image_require'],
                        'classes': ['collapse']}),
    ]
    list_display = ('name', 'no_require', 'show_recipe', 'with_recipe')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['name', 'description', 'category', ]}),
        ('Detalle', {'fields': ['price', 'inventory', 'active', 'recipe', ]}),
        ('Descuento', {'fields': ['discount', ]}),
    ]
    list_display = ('name', 'category', 'price', 'status_inventory', 'active', 'thumbnail',)
    search_fields = ('name', 'category__name',)


admin.site.register(Product, ProductAdmin)


class DiscountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['name', 'short_name', 'type', 'price', 'percentage', 'quantity', ]}),
        ('Vigencias', {'fields': ['date_begins', 'date_ends', ]}),
    ]
    list_display = ('name', 'type', 'price', 'percentage', 'quantity', 'date_begins', 'date_ends')
    search_fields = ('name', 'type', 'date_begins', 'date_ends',)


admin.site.register(Discount, DiscountAdmin)
