from django.db import models
from productos.models import Product
from usuarios.models import Direction, CustomUser

# Create your models here.

class Venta(models.Model):
	user = models.ForeignKey(CustomUser)
	enviar = models.ForeignKey(Direction, blank=True, null=True, on_delete=models.SET_NULL)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

class DetalleVenta(models.Model):
	venta = models.ForeignKey(Venta)
	product = models.ForeignKey(Product)
	price = models.DecimalField(max_digits = 10, decimal_places = 2)
	cantidad = models.IntegerField()
	img_receta = models.ImageField(upload_to = 'detalleventa/recetas/')
