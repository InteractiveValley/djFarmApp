# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0003_auto_20150916_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsale',
            name='discount',
            field=models.DecimalField(default=0, verbose_name=b'descuento', max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='detailsale',
            name='subtotal',
            field=models.DecimalField(default=0, verbose_name=b'subtotal', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='detailsale',
            name='sale',
            field=models.ForeignKey(related_name='detail_sales', to='carrito.Sale'),
        ),
    ]
