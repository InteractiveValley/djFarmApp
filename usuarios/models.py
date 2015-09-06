from django.db import models
from django.contrib.auth.models import User
from productos.models import Product

# Create your models here.

class Direction(models.Model):
	localidad = models.CharField(max_length = 140)
	calle = models.CharField(max_length = 140)
	num_interior = models.CharField(max_length = 50)
	num_exterior = models.CharField(max_length = 50)
	codigo_postal = models.CharField(max_length = 10)
	colonia = models.CharField(max_length = 150)
	delegacion_municipio = models.CharField(max_length = 150)
	user = models.ForeignKey(User)

	def __str__(self):
		return "%s %s %s" % (self.calle,self.num_interior, self.num_exterior)

class Profile(models.Model):
	user = models.OneToOneField(User)
	cell = models.CharField(max_length = 50)

	def __str__(self):
		return self.user.username

class PedidoPeriodico(models.Model):
	producto = models.ForeignKey(Product)
	user = models.ForeignKey(User)
	cantidad = models.IntegerField()
	periodo = models.CharField(max_length = 100) # diario, semanal, mensual
	lunes = models.BooleanField()
	martes = models.BooleanField()
	miercoles = models.BooleanField()
	jueves = models.BooleanField()
	viernes = models.BooleanField()
	sabado = models.BooleanField()
	domingo = models.BooleanField()
	proxima_entrega = models.DateTimeField()
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

# esta clase no tiene gran uso
class Pregunta(models.Model):
	pregunta = models.CharField(max_length = 140)
	respuesta = models.TextField()
	orden = models.IntegerField()
