from django.contrib import admin
from .models import Category, Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	fieldsets = [
        (None, {'fields': ['name']}),
        ('Thumbnails', {'fields': ['image_require','image_no_require'],'classes': ['collapse']}),
	]
	list_display = ('name','require','no_require',)
	search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
	fieldsets = [
        ('General', {'fields': ['name','description','category']}),
        ('Detalle', {'fields': ['price','active','require_prescription']}),
	]
	list_display = ('name','category','price','is_active','is_require_prescription','thumbnail')
	search_fields = ('name',)


admin.site.register(Product, ProductAdmin)

