from django.db import models
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=140, verbose_name="categoria")
    image_require = models.ImageField(upload_to='categorias/require/', verbose_name="Quedarse receta", null=True,
                                      blank=True)
    image_require_show = models.ImageField(upload_to='categorias/require/', verbose_name="Mostrar receta", null=True,
                                           blank=True)
    image_no_require = models.ImageField(upload_to='categorias/norequire/', verbose_name="Sin receta", null=True,
                                         blank=True)

    def no_require(self):
        if self.image_no_require != None:
            return """
            <img src="%s" style="max-width: 60px; max-height: 60px;"/>
            """ % self.image_no_require.url
        else:
            return """
            <img src="http://placehold.it/60x60" style="max-width: 60px; max-height: 60px;"/>
            """

    def show_recipe(self):
        if self.image_require_show != None:
            return """
            <img src="%s" style="max-width: 60px; max-height: 60px;"/>
            """ % self.image_require_show.url
        else:
            return """
            <img src="http://placehold.it/60x60" style="max-width: 60px; max-height: 60px;"/>
            """

    def with_recipe(self):
        if self.image_require != None:
            return """
            <img src="%s" style="max-width: 60px; max-height: 60px;"/>
            """ % self.image_require.url
        else:
            return """
            <img src="http://placehold.it/60x60" style="max-width: 60px; max-height: 60px;"/>
            """

    def __str__(self):
        return self.name

    with_recipe.allow_tags = True
    show_recipe.allow_tags = True
    no_require.allow_tags = True

    class Meta:
        verbose_name = 'categoria'


PRICE = 'precio'
PERCENTAGE = 'porcentaje'
QUANTITY = 'cantidad'

TYPE_DISCOUNTS = (
    (PRICE, 'Por precio',),
    (PERCENTAGE, 'Por porcentaje',),
    (QUANTITY, 'Por cantidad'),
)


class Discount(models.Model):
    name = models.CharField('promocion', max_length=140, default='Promocion', null=True, blank=True, )
    short_name = models.CharField('etiqueta', max_length=20, default='-10%', null=True, blank=True, )
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


NORMAL = 1
HAVE_RECIPE = 2
STAY_RECIPE = 3

REQUIRE_PRESCRIPTION = (
    (NORMAL, 'No require receta'),
    (HAVE_RECIPE, 'El repartidor te pedira que le muestres la receta'),
    (STAY_RECIPE, 'El repartidor te pedira y se quedara con la receta'),
)


class Product(models.Model):
    name = models.CharField(max_length=140, verbose_name="producto")
    description = models.TextField(verbose_name="descripcion")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="precio")
    require_prescription = models.BooleanField(verbose_name="require receta")  # requiere receta
    recipe = models.IntegerField("receta", default=NORMAL, choices=REQUIRE_PRESCRIPTION)
    active = models.BooleanField(verbose_name="es activo")  # esta disponible
    category = models.ForeignKey(Category, verbose_name="categoria")
    discount = models.ForeignKey(Discount, verbose_name="descuento", null=True, blank=True)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)

    def __str__(self):
        return self.name

    def thumbnail(self):
        if self.recipe == NORMAL:
            return self.category.no_require()
        elif self.recipe == HAVE_RECIPE:
            return self.category.show_recipe()
        else:
            return self.category.with_recipe()

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
