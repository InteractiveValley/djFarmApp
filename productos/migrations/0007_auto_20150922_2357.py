# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_auto_20150922_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='name',
            field=models.CharField(default=b'Promocion', max_length=140, null=True, verbose_name=b'promocion', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.ForeignKey(verbose_name=b'descuento', blank=True, to='productos.Discount', null=True),
        ),
    ]
