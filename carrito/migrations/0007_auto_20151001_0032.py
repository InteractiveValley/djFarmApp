# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0006_auto_20150928_1529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detailsale',
            options={'verbose_name': 'detalle de venta', 'verbose_name_plural': 'detalles de venta'},
        ),
        migrations.AlterModelOptions(
            name='imagesale',
            options={'verbose_name': 'receta', 'verbose_name_plural': 'recetas'},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'verbose_name': 'venta', 'verbose_name_plural': 'ventas'},
        ),
    ]
