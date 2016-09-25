# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0022_auto_20160626_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='date_expiration',
            field=models.DateField(null=True, verbose_name=b'caduca', blank=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='type_receipt',
            field=models.IntegerField(default=1, verbose_name=b'Tipo de trasaccion', choices=[(4, b'Producto destruido'), (2, b'Producto vendido'), (5, b'Producto inactivado'), (1, b'Producto recibido'), (3, b'Producto caducado')]),
        ),
    ]
