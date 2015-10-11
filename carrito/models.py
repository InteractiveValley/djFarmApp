from django.db import models
from productos.models import Product
from usuarios.models import Direction, CustomUser
from django.utils import timezone
from productos.models import Discount

INCOMPLETE = 0
COMPLETE = 1
APPROVED = 2
REJECTED = 3
DELIVERED = 4
PAID = 5
NO_PAID = 6

STATUS_SALE = {
    (INCOMPLETE, "Incompleto"),
    (COMPLETE, "Completo"),
    (APPROVED, "Aprobado"),
    (REJECTED, "Rechazado"),
    (DELIVERED, "Entregado"),
    (PAID, "Pagado"),
    (NO_PAID, "No pagado"),
}


class Sale(models.Model):
    user = models.ForeignKey(CustomUser)
    direction = models.ForeignKey(Direction, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.IntegerField("Estatus", default=0, choices=STATUS_SALE)
    scheduled_order = models.BooleanField("pedido programado", default=False)
    delivered = models.BooleanField("entregado", default=False)
    charge_conekta = models.CharField("Cargo Id Conekta", max_length=140, default="", null=True, blank=True)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return "Venta: %i .- Usuario: %s" % (self.id, self.user.get_full_name())

    def subtotal(self):
        detalle_ventas = self.detail_sales.all()
        dSubtotal = 0.0
        for detalle in detalle_ventas:
            dSubtotal += float(detalle.subtotal)
        return dSubtotal

    def discount(self):
        detalle_ventas = self.detail_sales.all()
        dDiscount = 0.0
        for detalle in detalle_ventas:
            dDiscount += float(detalle.discount)
        return dDiscount

    def total(self):
        detalle_ventas = self.detail_sales.all()
        dTotal = 0.0
        for detalle in detalle_ventas:
            dTotal += detalle.total()
        return dTotal

    def show_status(self):
        if self.status == INCOMPLETE:
            return "Capturando"
        elif self.status == COMPLETE:
            return "Pedido"
        elif self.status == APPROVED:
            return "Aprobado"
        elif self.status == REJECTED:
            return "Rechazado"
        elif self.status == DELIVERED:
            return "Entregado"

    show_status.allow_tags = True

    class Meta:
        verbose_name = "venta"
        verbose_name_plural = "ventas"


class DetailSale(models.Model):
    sale = models.ForeignKey(Sale, related_name="detail_sales")
    product = models.ForeignKey(Product)
    price = models.DecimalField("precio", max_digits=10, decimal_places=2)
    quantity = models.IntegerField("cantidad")
    subtotal = models.DecimalField("subtotal", max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField("descuento", max_digits=10, decimal_places=2, default=0)

    def need_validation(self):
        return self.product.require_prescription

    def __str__(self):
        return "Venta: %i .- Producto: %s, Cant: %i" % (self.sale.id, self.product.name, self.quantity)

    def save(self, *args, **kwargs):
        """
        On save, update price
        """
        if self.id is None:
            self.price = self.product.price
        self.subtotal = self.quantity * self.price
        self.calculate_discount()
        return super(DetailSale, self).save(*args, **kwargs)

    def calculate_discount(self):
        descuento = self.product.discount
        now = timezone.now().date()
        if descuento is not None and descuento.date_ends > now:
            if descuento.type == Discount.PRICE:
                price = descuento.price
                subtotal = float(self.quantity * price)
                self.discount = float(self.price * self.quantity) - subtotal
            elif descuento.type == Discount.PERCENTAGE:
                price = (float(self.price) * (1.00 - (float(descuento.percentage) / 100.00)))
                subtotal = float(self.quantity * price)
                self.discount = float(self.price * self.quantity) - subtotal
                #  import ipdb; ipdb.set_trace();
            elif descuento.type == Discount.QUANTITY:
                enteros = int(self.quantity / descuento.quantity)
                fracciones = self.quantity - enteros
                if descuento.price > 0:
                    conDescuento = float(enteros * descuento.price)
                    sinDescuento = float(fracciones * self.price)
                    subtotal = conDescuento + sinDescuento
                    self.discount = float(self.price * self.quantity) - subtotal
                else:
                    price = (self.price * (1.00 - (float(descuento.percentage) / 100.00)))
                    conDescuento = float(enteros * price)
                    sinDescuento = float(fracciones * self.price)
                    subtotal = conDescuento + sinDescuento
                    self.discount = float(self.price * self.quantity) - subtotal

    def total(self):
        return float(self.subtotal) - float(self.discount)

    class Meta:
        verbose_name = "detalle de venta"
        verbose_name_plural = "detalles de venta"


class ImageSale(models.Model):
    sale = models.ForeignKey(Sale, related_name="images")
    image_recipe = models.ImageField("receta", upload_to='recetas/', null=True, blank=True)

    class Meta:
        verbose_name = "receta"
        verbose_name_plural = "recetas"