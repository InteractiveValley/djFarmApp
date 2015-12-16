from django.db import models
from productos.models import Product
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    cell = models.CharField(max_length=50)
    inapam = models.BooleanField("INAPAM", default=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class ConektaUser(models.Model):
    user = models.ForeignKey(CustomUser, related_name='conektas', verbose_name='user')
    conekta_user = models.CharField(max_length=140, verbose_name='conekta')
    is_active = models.BooleanField("es_activo", default=True)
    is_default = models.BooleanField("es_default", default=False)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(ConektaUser, self).save(*args, **kwargs)


class Direction(models.Model):
    location = models.CharField("localidad", max_length=140)
    street = models.CharField("calle", max_length=140)
    interior_number = models.CharField("numero interior", max_length=50, null=True, blank=True)
    exterior_number = models.CharField("numero exterior", max_length=50, null=True, blank=True)
    postal_code = models.CharField("codigo postal", max_length=10, null=True, blank=True)
    colony = models.CharField("colonia", max_length=150, null=True, blank=True)
    delegation_municipaly = models.CharField("delegacion o municipio", max_length=150, null=True, blank=True)
    user = models.ForeignKey(CustomUser, related_name="directions")
    lat = models.CharField("latitude", max_length=100, null=True, blank=True)
    lng = models.CharField("longitude", max_length=100, null=True, blank=True)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)
    active = models.BooleanField(verbose_name="activa", default=True)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Direction, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s %s" % (self.street, self.interior_number, self.exterior_number)

    def direction(self):
        return "%s %s %s, col: %s, cp: %s, Del/Mun: %s, %s" % \
               (self.street, self.interior_number, self.exterior_number,
                self.colony, self.postal_code, self.delegation_municipaly, self.location)

    direction.short_description = "direccion"

    class Meta:
        verbose_name = "direccion"
        verbose_name_plural = "direcciones"


class ScheduledOrder(models.Model):
    DAILY = 'por dia'
    WEEKLY = 'semanal'
    MONTHLY = 'mensual'

    PERIODS = (
        (DAILY, 'Por dia',),
        (WEEKLY, 'Semanal',),
        (MONTHLY, 'Mensual'),
    )

    product = models.ForeignKey(Product, verbose_name="producto")
    user = models.ForeignKey(CustomUser, related_name='schedules_orders')
    quantity = models.IntegerField("cantidad", default=1)
    period = models.CharField("periodo", choices=PERIODS, max_length=100)  # por dia, semanal, mensual
    days = models.PositiveIntegerField("dias", default=1)
    times = models.IntegerField("veces", default=0)
    date_next = models.DateField("proxima entrega", null=True, blank=True)
    date_ends = models.DateField("finaliza", null=True, blank=True)
    created = models.DateTimeField("creado", null=True, blank=True)
    modified = models.DateTimeField("actualizado", null=True, blank=True)
    canceled_for_user = models.BooleanField("cancelado por usuario", default=False)
    canceled_for_system = models.BooleanField("finalizacion", default=False)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.calculate_date_next()
        return super(ScheduledOrder, self).save(*args, **kwargs)

    def calculate_date_next(self):
        if self.period == self.WEEKLY:
            self.days = 7
        elif self.period == self.MONTHLY:
            self.days = 30
        now = self.modified
        self.date_next = now.date() + timezone.timedelta(days=self.days)
        self.date_ends = now.date() + timezone.timedelta(days=self.days * self.times)

    class Meta:
        verbose_name = "pedido programado"
        verbose_name_plural = "pedidos programados"


# esta clase no tiene gran uso
class Question(models.Model):
    question = models.CharField("pregunta", max_length=140)
    ask = models.TextField("respuesta")
    order = models.IntegerField("orden")

    class Meta:
        verbose_name = "pregunta"
        verbose_name_plural = "preguntas"


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="usuario", related_name="ratings", related_query_name="rating")
    comment = models.TextField("comentario", blank=True, null=True)
    rating = models.IntegerField("calificacion", default=0)
    created = models.DateTimeField("creado", null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = timezone.now()
        return super(Rating, self).save(*args, **kwargs)


class Inapam(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="usuario", related_name="images_inapam",
                             related_query_name="images_inapam")
    inapam = models.ImageField(upload_to="inapam/")
    active = models.BooleanField(verbose_name="Autorizado", default=False)
