# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_auto_20150922_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.ForeignKey(related_name='descuento', blank=True, to='productos.Discount', null=True),
        ),
    ]
