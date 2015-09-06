from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length = 140)
	image_require = models.ImageField(upload_to = 'categorias/require/')
	image_no_require = models.ImageField(upload_to = 'categorias/norequire/')
	
	def __str__(self):
		return self.name
	
class Product(models.Model):
	name = models.CharField(max_length = 140)
	description = models.TextField()
	price = models.DecimalField(max_digits = 10, decimal_places = 2)
	require_prescription = models.BooleanField() # requiere receta
	is_active = models.BooleanField() # esta disponible
	category = models.ForeignKey(Category)
	
	def __str__(self):
		return self.name