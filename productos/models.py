from django.db import models
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=140, verbose_name="categoria")
    image_require = models.ImageField(upload_to='categorias/require/', verbose_name="imagen require")
    image_no_require = models.ImageField(upload_to='categorias/norequire/', verbose_name="imagen no require")

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
        verbose_name = 'categoria'


PRICE = 'precio';
PERCENTAGE = 'porcentaje';
QUANTITY = 'cantidad';

TYPE_DISCOUNTS = (
    (PRICE, 'Por precio',),
    (PERCENTAGE, 'Por porcentaje',),
    (QUANTITY, 'Por cantidad'),
)


class Discount(models.Model):
    name = models.CharField('promocion', max_length=140, default='Promocion', null=True, blank=True,)
    short_name = models.CharField('etiqueta', max_length=20, default='-10%', null=True, blank=True,)
    type = models.CharField('tipo', max_length=100, choices=TYPE_DISCOUNTS)
    price = models.DecimalField('precio', max_digits=10, decimal_places=2, default=0)
    percentage = models.PositiveSmallIntegerField('porcentaje', default=0)
    quantity = models.PositiveSmallIntegerField('cantidad', default=1)
    date_begins = models.DateField('inicia', null=True, blank=True)
    date_ends = models.DateField('finaliza', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        On save, update date_begins
        """
        if not self.id and self.date_begins is None:
            self.date_begins = timezone.now().date()
        return super(Discount, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "descuento"
        verbose_name_plural = "descuentos"


class Product(models.Model):
    name = models.CharField(max_length=140, verbose_name="producto")
    description = models.TextField(verbose_name="descripcion")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="precio")
    require_prescription = models.BooleanField(verbose_name="require receta")  # requiere receta
    active = models.BooleanField(verbose_name="es activo")  # esta disponible
    category = models.ForeignKey(Category, verbose_name="categoria")
    discount = models.ForeignKey(Discount, verbose_name="descuento", null=True, blank=True)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)

    def __str__(self):
        return self.name

    def thumbnail(self):
        if self.require_prescription:
            return self.category.require()
        else:
            return self.category.no_require()

    thumbnail.allow_tags = True
    thumbnail.short_description = 'Imagen'

    def product_image(self):
        if self.require_prescription:
            return self.category.image_require
        else:
            return self.category.image_no_require

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'producto'
