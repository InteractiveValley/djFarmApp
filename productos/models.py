from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length = 140 , verbose_name="categoria")
	image_require = models.ImageField(upload_to = 'categorias/require/', verbose_name="imagen require")
	image_no_require = models.ImageField(upload_to = 'categorias/norequire/', verbose_name="imagen no require")

	def require(self):
		return """
		<img src="%s" style="max-width: 60px; max-height: 60px;"/> 
		""" % self.image_require.url

	def no_require(self):
		return """
		<img src="%s" style="max-width: 60px; max-height: 60px;"/> 
		""" % self.image_no_require.url		
	
	def __str__(self):
		return self.name

	require.allow_tags = True
	no_require.allow_tags = True

	class Meta:
		verbose_name='categoria'
	
class Product(models.Model):
	name = models.CharField(max_length = 140, verbose_name="producto")
	description = models.TextField(verbose_name="descripcion")
	price = models.DecimalField(max_digits = 10, decimal_places = 2,verbose_name="precio")
	require_prescription = models.BooleanField(verbose_name="require receta") # requiere receta
	active = models.BooleanField(verbose_name="es activo") # esta disponible
	category = models.ForeignKey(Category,verbose_name="categoria")
	
	def __str__(self):
		return self.name

	def is_active(self):
		return self.active

	def is_require_prescription(self):
		return self.require_prescription

	def thumbnail(self):
		if self.require_prescription:
			return self.category.require()
		else:
			return self.category.no_require()

	is_active.boolean = True
	is_active.short_description='Activo'
	is_require_prescription.boolean = True
	is_require_prescription.short_description = 'Require receta'
	thumbnail.allow_tags = True
	thumbnail.short_description = 'Imagen'

	class Meta:
		verbose_name = 'producto'