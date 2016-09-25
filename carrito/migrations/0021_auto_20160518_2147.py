# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0020_auto_20160501_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='distribuidor',
            field=models.CharField(max_length=140, null=True, verbose_name=b'distribuidor', blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='factura',
            field=models.CharField(max_length=140, null=True, verbose_name=b'factura', blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='no_lote',
            field=models.CharField(max_length=140, null=True, verbose_name=b'no. de lote', blank=True),
        ),
        migrations.AlterField(
            model_name='detailsend',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name=b'cantidad a enviar'),
        ),
    ]
