# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0014_sale_shipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='date_expiration',
            field=models.DateField(null=True, verbose_name=b'expira', blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='type_recipe',
            field=models.IntegerField(default=1, verbose_name=b'Tipo de trasaccion', choices=[(4, b'Producto destruido'), (2, b'Producto vendido'), (1, b'Producto recibido'), (3, b'Producto caducado')]),
        ),
    ]
