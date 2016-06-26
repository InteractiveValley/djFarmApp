# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0021_auto_20160518_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesale',
            name='is_antibiotico',
            field=models.BooleanField(default=False, verbose_name=b'Antibiotico'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='quantity_original',
            field=models.IntegerField(default=0, verbose_name=b'recibo original'),
        ),
    ]
