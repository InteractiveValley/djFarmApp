# -*- encoding: utf-8 -*-
from django.db import models
from productos.models import Product
from usuarios.models import Direction, CustomUser, CardConekta
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
    user = models.ForeignKey(CustomUser, verbose_name="cliente", related_name="user")
    vendor = models.ForeignKey(CustomUser, verbose_name="vendedor", related_name="vendor", null=True, blank=True)
    direction = models.ForeignKey(Direction, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.IntegerField("Estatus", default=0, choices=STATUS_SALE)
    scheduled_order = models.BooleanField("pedido programado", default=False)
    delivered = models.BooleanField("entregado", default=False)
    card_conekta = models.ForeignKey(CardConekta, verbose_name="tarjeta", null=True, blank=True)
    charge_conekta = models.CharField("Cargo Id Conekta", max_length=140, default="", null=True, blank=True)
    notes = models.TextField("Notas/Comentarios", blank=True, null=True)
    shipping = models.DecimalField("envio", max_digits=10, decimal_places=2, default=25)
    with_shipping = models.BooleanField("con envio", default=False, null=False, blank=False)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.localtime(timezone.now())
        self.modified = timezone.localtime(timezone.now())
        return super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        cadena = "Venta: %i .- Usuario: %s" % (self.id, self.user.get_full_name())
        return cadena

    def subtotal(self):
        detalle_ventas = self.detail_sales.all()
        d_subtotal = 0.0
        for detalle in detalle_ventas:
            d_subtotal += float(detalle.subtotal)
        return d_subtotal

    def discount(self):
        detalle_ventas = self.detail_sales.all()
        d_discount = 0.0
        for detalle in detalle_ventas:
            d_discount += float(detalle.discount)
        return d_discount

    def discount_inapam(self):
        detalle_ventas = self.detail_sales.all()
        d_discount_inapam = 0.0
        for detalle in detalle_ventas:
            d_discount_inapam += float(detalle.discount_inapam)
        return d_discount_inapam

    def tax(self):
        detalle_ventas = self.detail_sales.all()
        d_tax = 0.0
        for detalle in detalle_ventas:
            d_tax += float(detalle.tax)
        return d_tax

    def total(self):
        detalle_ventas = self.detail_sales.all()
        d_total = 0.0
        for detalle in detalle_ventas:
            d_total += detalle.total()

        if self.shipping > 0.0:
            return d_total + float(self.shipping)
        else:
            return d_total

    def discount_inventory(self):
        detalle_ventas = self.detail_sales.all()
        for detalle in detalle_ventas:
            product = detalle.product
            detalle.product.inventory = detalle.product.inventory - detalle.quantity
            product.save()
        return True

    def has_recipe(self):
        detalle_ventas = self.detail_sales.all()
        b_recipe = False
        for detalle in detalle_ventas:
            if detalle.product.recipe == Product.STAY_RECIPE:
                b_recipe = True
                break
        return b_recipe

    def show_status(self):
        if self.status == INCOMPLETE:
            return "Capturando"
        elif self.status == COMPLETE:
            return "Pedido"
        elif self.status == APPROVED:
            return "Enviado"
        elif self.status == REJECTED:
            return "Cancelado"
        elif self.status == DELIVERED:
            return "Entregado"
        elif self.status == PAID:
            return "Pagado"
        elif self.status == NO_PAID:
            return "No Pagado"

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
    tax = models.DecimalField("IVA", max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField("descuento", max_digits=10, decimal_places=2, default=0)
    discount_inapam = models.DecimalField("descuento inapam", max_digits=10, decimal_places=2, default=0)
    with_shipping = models.BooleanField("con envio", default=False, null=False, blank=False)
    quantity_shipping = models.IntegerField("cantidad enviada", default=0, null=False, blank=False)

    def need_validation(self):
        return self.product.require_prescription

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        cadena = "Venta: %i .- Producto: %s, Cant: %i" % (self.sale.id, self.product.name, self.quantity)
        return cadena

    def save(self, *args, **kwargs):
        """
        On save, update price
        """
        if self.id is None:
            self.price = self.product.price

        self.subtotal = self.quantity * self.price
        self.calculate_discount()

        if self.sale.user.inapam:
            total = float(self.subtotal) - float(self.discount)
            self.discount_inapam = float(total * 0.10)

        if self.product.with_tax:
            total = float(self.subtotal) - float(self.discount) - float(self.discount_inapam)
            self.tax = total * 0.16

        return super(DetailSale, self).save(*args, **kwargs)

    def calculate_discount(self):
        descuento = self.product.discount
        now = timezone.localtime(timezone.now()).date()
        if descuento is not None and (descuento.date_begins <= now and descuento.date_ends >= now):
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
        else:
            # import ipdb; ipdb.set_trace();
            return 0.0

    def total(self):
        return float(self.subtotal) - float(self.discount) - float(self.discount_inapam) + float(self.tax)

    def complete_shipping(self):
        productos = self.quantity
        detalles_envio = self.detail_sends.all()
        envios = 0
        for envio in detalles_envio:
            envios += envio.quantity
        porcentaje = float(envios / productos)
        return str(int(porcentaje * 100)) + "%"

    class Meta:
        verbose_name = "detalle de venta"
        verbose_name_plural = "detalles de venta"


class ImageSale(models.Model):
    sale = models.ForeignKey(Sale, related_name="images")
    image_recipe = models.ImageField("receta", upload_to='recetas/', null=True, blank=True)

    class Meta:
        verbose_name = "receta"
        verbose_name_plural = "recetas"


TYPE_RECEIPT = 1
TYPE_SALE = 2
TYPE_OBSOLETE = 3
TYPE_DELETE = 4

TYPE_RECEIPTS = {
    (TYPE_RECEIPT, "Producto recibido"),
    (TYPE_SALE, "Producto vendido"),
    (TYPE_OBSOLETE, "Producto caducado"),
    (TYPE_DELETE, "Producto destruido"),
}


class Receipt(models.Model):
    product = models.ForeignKey(Product, verbose_name="producto")
    user = models.ForeignKey(CustomUser, verbose_name="usuario")
    quantity = models.IntegerField("recibido", default=0)
    type_receipt = models.IntegerField("Tipo de trasaccion", default=TYPE_RECEIPT, choices=TYPE_RECEIPTS)
    status = models.BooleanField("procesado", default=False)
    date_expiration = models.DateField("expira", null=True, blank=True)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.localtime(timezone.now())
        self.modified = timezone.localtime(timezone.now())

        if self.type_receipt == TYPE_RECEIPT:
            if not self.status:
                product = self.product
                product.inventory = product.inventory + self.quantity
                product.save()
                self.status = True
        elif self.type_receipt == TYPE_OBSOLETE:
            if not self.status:
                product = self.product
                product.inventory = product.inventory - self.quantity
                product.save()
                self.status = True

        return super(Receipt, self).save(*args, **kwargs)

    def show_type_recipe(self):
        if self.type_recipe == TYPE_RECEIPT:
            return "Producto recibido"
        elif self.type_recipe == TYPE_SALE:
            return "Producto vendido"
        elif self.type_recipe == TYPE_OBSOLETE:
            return "Producto obsoleto"
        elif self.type_recipe == TYPE_DELETE:
            return "Producto destruido"

    def expiration(self):
        now = timezone.localtime(timezone.now())
        if self.date_expiration is not None:
            expira = self.date_expiration - now.date()
            horas = expira.seconds / 3600
            minutos = expira.seconds / 60
            if horas > (24 * 30):
                return """
                <span style="padding: 5px 20px; background-color: transparent;">%i dias</span>
                """ % expira.days
            elif horas <= (24 * 30):
                return """
                <span style="padding: 5px 20px; background-color: orange; color: black;">%i dias</span>
                """ % expira.days
            elif horas < 24 and horas > 1:
                return """
                <span style="padding: 5px 20px; background-color: orange; color: black;">%i horas</span>
                """ % horas
            elif minutos < 60 and minutos > 1:
                return """
                <span style="padding: 5px 20px; background-color: orange; color: black;">%i minutos</span>
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
    expiration.admin_order_field = 'date_expiration'

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        if self.type_receipt == TYPE_RECEIPT:
            cadena = "Recibo: %i, Producto: %s, Cant: %i, Caduca: %s" % (
                self.id, self.product.name, self.quantity, str(self.date_expiration))
        elif self.type_receipt == TYPE_OBSOLETE:
            cadena = "Recibo: %i, Producto: %s, Cant: %i, Caduco: %s" % (
                self.id, self.product.name, self.quantity, str(self.date_expiration))
        return cadena

    class Meta:
        verbose_name = 'recibo'


class Send(models.Model):
    sale = models.ForeignKey(Sale, verbose_name="venta")
    vendor = models.ForeignKey(CustomUser, verbose_name="vendedor", null=True, blank=True)
    status = models.BooleanField("Enviado", default=False)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.localtime(timezone.now())
        self.modified = timezone.localtime(timezone.now())

        return super(Send, self).save(*args, **kwargs)

    def complete(self):
        detalles_venta = self.sale.detail_sales.all()
        productos = 0
        for detalle in detalles_venta:
            productos += int(detalle.quantity)
        detalles_envio = self.detail_sends.all()
        envios = 0
        for envio in detalles_envio:
            envios += envio.quantity
        if productos > 0:
            porcentaje = float(envios / productos)
        else:
            porcentaje = 0.0
        return str(int(porcentaje * 100)) + "%"

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        cadena = "Envio: %i, Venta: %i" % (self.id, self.sale.id)
        return cadena


class DetailSend(models.Model):
    send = models.ForeignKey(Send, verbose_name="envio", related_name="detail_sends")
    detail_sale = models.ForeignKey(DetailSale, verbose_name="linea", related_name="detail_sends")
    receipt = models.ForeignKey(Receipt, verbose_name="recibo asociado", related_name="detail_sends")
    quantity = models.IntegerField("cantidad a enviar", default=0)
    type_receipt = models.IntegerField("Tipo de trasaccion", default=TYPE_SALE)
    status = models.BooleanField("procesado", default=False)
    date_expiration = models.DateField("expira", null=True, blank=True)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.localtime(timezone.now())
        self.modified = timezone.localtime(timezone.now())

        return super(DetailSend, self).save(*args, **kwargs)
