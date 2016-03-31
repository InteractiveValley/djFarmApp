# -*- encoding: utf-8 -*-
from django.db import models
from django.utils import timezone


def image_default():
    return """
    <img src="http://placehold.it/60x60" style="max-width: 60px; max-height: 60px;"/>
    """


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=140, verbose_name="categoria")
    position = models.PositiveSmallIntegerField('posicion', default=0)
    image_category = models.ImageField(upload_to='categorias/', verbose_name="Imagen", null=True,
                                       blank=True)

    def save(self, *args, **kwargs):
        """
        On save, update date_begins
        """
        if self.position == 0:
            self.position = Category.objects.count() + 1
        return super(Category, self).save(*args, **kwargs)

    def thumbnail(self):
        if self.image_category is not None:
            try:
                return """
                <img src="%s" style="max-width: 60px; max-height: 60px;"/>
                """ % self.image_category.url
            except ValueError:
                return image_default()
        else:
            return image_default()

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return self.name

    thumbnail.allow_tags = True

    class Meta:
        verbose_name = 'categoria'


class Discount(models.Model):
    PRICE = 'precio'
    PERCENTAGE = 'porcentaje'
    QUANTITY = 'cantidad'

    TYPE_DISCOUNTS = (
        (PRICE, 'Por precio',),
        (PERCENTAGE, 'Por porcentaje',),
        (QUANTITY, 'Por cantidad'),
    )

    name = models.CharField('promocion', max_length=140, default='Promocion', null=True, blank=True, )
    short_name = models.CharField('etiqueta', max_length=20, default='-10%', null=True, blank=True, )
    type = models.CharField('tipo', max_length=100, choices=TYPE_DISCOUNTS)
    price = models.DecimalField('precio', max_digits=10, decimal_places=2, default=0)
    percentage = models.PositiveSmallIntegerField('porcentaje', default=0)
    quantity = models.PositiveSmallIntegerField('cantidad', default=1)
    date_begins = models.DateField('inicia', null=True, blank=True)
    date_ends = models.DateField('finaliza', null=True, blank=True)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        On save, update date_begins
        """
        if not self.id and self.date_begins is None:
            self.date_begins = timezone.localtime(timezone.now()).date()
        return super(Discount, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "descuento"
        verbose_name_plural = "descuentos"


class Laboratory(models.Model):
    name = models.CharField("laboratorio", max_length=250)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "laboratorio"
        verbose_name_plural = "laboratorios"


class Product(models.Model):
    NORMAL = 1
    HAVE_RECIPE = 2
    STAY_RECIPE = 3

    REQUIRE_PRESCRIPTION = (
        (NORMAL, 'No require receta'),
        (HAVE_RECIPE, 'El repartidor te pedira que le muestres la receta'),
        (STAY_RECIPE, 'El repartidor te pedira y se quedara con la receta'),
    )

    name = models.CharField(max_length=140, verbose_name="producto")
    description = models.TextField(verbose_name="descripcion")
    substances = models.CharField("sustancia activa", max_length=140, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="precio")
    with_tax = models.BooleanField(verbose_name="con IVA", default=True)  # esta disponible
    require_prescription = models.BooleanField(verbose_name="require receta", default=False)  # descontinuada
    recipe = models.IntegerField("receta", default=NORMAL, choices=REQUIRE_PRESCRIPTION)
    active = models.BooleanField(verbose_name="es activo")  # esta disponible
    inventory = models.IntegerField("inventario", default=0)
    category = models.ForeignKey(Category, verbose_name="categoria")
    laboratory = models.ForeignKey(Laboratory, verbose_name="laboratorio", null=True, blank=True)
    discount = models.ForeignKey(Discount, verbose_name="descuento", null=True, blank=True)
    image_require = models.ImageField(upload_to='productos/require/', verbose_name="Quedarse receta", null=True,
                                      blank=True)
    image_require_show = models.ImageField(upload_to='productos/require/', verbose_name="Mostrar receta", null=True,
                                           blank=True)
    image_no_require = models.ImageField(upload_to='productos/norequire/', verbose_name="Sin receta", null=True,
                                         blank=True)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)
    date_enter = models.DateTimeField("Fecha entrada", null=True, blank=True)
    date_out = models.DateTimeField("Fecha salida", null=True, blank=True)
    date_expiration = models.DateTimeField("Caducidad", null=True, blank=True)

    def no_require(self):
        image = self.image_no_require
        # import pdb; pdb.set_trace()
        if image is not None:
            try:
                return """
                <img src="%s" style="max-width: 60px; max-height: 60px;"/>
                """ % self.image_no_require.url
            except ValueError:
                return image_default()
        else:
            return image_default()

    def show_recipe(self):
        image = self.image_require_show
        # import pdb; pdb.set_trace()
        if image is not None:
            try:
                return """
                <img src="%s" style="max-width: 60px; max-height: 60px;"/>
                """ % self.image_require_show.url
            except ValueError:
                return image_default()
        else:
            return image_default()

    def with_recipe(self):
        image = self.image_require
        # import pdb; pdb.set_trace()
        if image is not None:
            try:
                return """
                <img src="%s" style="max-width: 60px; max-height: 60px;"/>
                """ % self.image_require.url
            except ValueError:
                return image_default()
        else:
            return image_default()

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return self.name

    with_recipe.allow_tags = True
    show_recipe.allow_tags = True
    no_require.allow_tags = True

    def thumbnail(self):
        if self.recipe == self.NORMAL:
            return self.no_require()
        elif self.recipe == self.HAVE_RECIPE:
            return self.show_recipe()
        else:
            return self.with_recipe()

    thumbnail.allow_tags = True
    thumbnail.short_description = 'imagen'

    def product_image(self):
        if self.recipe == self.NORMAL:
            return self.image_no_require
        elif self.recipe == self.HAVE_RECIPE:
            return self.image_require_show
        else:
            return self.image_require

    def status_inventory(self):
        if self.inventory > 5:
            return """
            <span style="padding: 5px 20px; background-color: transparent;">%i</span>
            """ % self.inventory
        elif self.inventory > 0:
            return """
            <span style="padding: 5px 20px; background-color: yellow; color: black;">%i</span>
            """ % self.inventory
        else:
            return """
            <span style="padding: 5px 20px; background-color: red; color: white;">%i</span>
            """ % self.inventory

    status_inventory.allow_tags = True
    status_inventory.short_description = 'inventario'
    status_inventory.admin_order_field = 'inventory'

    def expiration(self):
        now = timezone.localtime(timezone.now())
        if self.date_expiration is not None:
            expira = self.date_expiration - now
            horas = expira.seconds / 3600
            minutos = expira.seconds / 60
            if horas > (24 * 5):
                return """
                <span style="padding: 5px 20px; background-color: transparent;">%i dias</span>
                """ % expira.days
            elif horas > 24:
                return """
                <span style="padding: 5px 20px; background-color: yellow; color: black;">%i dias</span>
                """ % expira.days
            elif horas < 24 and horas > 1:
                return """
                <span style="padding: 5px 20px; background-color: yellow; color: black;">%i horas</span>
                """ % horas
            elif minutos < 60 and minutos > 1:
                return """
                <span style="padding: 5px 20px; background-color: yellow; color: black;">%i minutos</span>
                """ % minutos
            else:
                return """
                <span style="padding: 5px 20px; background-color: red; color: white;">%i dias</span>
                """ % 0
        else:
            return """
                <span style="padding: 5px 20px; background-color: red; color: white;">%i dias</span>
                """ % 0

    expiration.allow_tags = True
    expiration.short_description = 'caduca'
    expiration.admin_order_field = 'date_out'

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.localtime(timezone.now())
        self.modified = timezone.localtime(timezone.now())
        return super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'producto'
