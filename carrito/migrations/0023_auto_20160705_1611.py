# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carrito', '0022_auto_20160626_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagesale',
            name='is_antibiotico',
        ),
        migrations.AddField(
            model_name='imagesale',
            name='created',
            field=models.DateTimeField(null=True, verbose_name=b'creado', blank=True),
        ),
        migrations.AddField(
            model_name='imagesale',
            name='folio_recipe',
            field=models.IntegerField(default=0, verbose_name=b'Folio de receta'),
        ),
        migrations.AddField(
            model_name='imagesale',
            name='modified',
            field=models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True),
        ),
        migrations.AddField(
            model_name='imagesale',
            name='type_recipe',
            field=models.IntegerField(default=1, verbose_name=b'Tipo de receta', choices=[(3, b'Receta con antibiotico'), (1, b'Receta sin folio'), (2, b'Receta normal')]),
        ),
        migrations.AddField(
            model_name='imagesale',
            name='user',
            field=models.ForeignKey(verbose_name=b'Usuario valido', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='type_receipt',
            field=models.IntegerField(default=1, verbose_name=b'Tipo de trasaccion', choices=[(4, b'Producto destruido'), (2, b'Producto vendido'), (5, b'Producto inactivado'), (1, b'Producto recibido'), (3, b'Producto caducado')]),
        ),
    ]
