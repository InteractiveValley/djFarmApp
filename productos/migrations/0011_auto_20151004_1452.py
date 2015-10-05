# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0010_auto_20151004_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inventory',
            field=models.IntegerField(default=0, verbose_name=b'inventario'),
        ),
        migrations.AlterField(
            model_name='product',
            name='require_prescription',
            field=models.BooleanField(default=False, verbose_name=b'require receta'),
        ),
    ]
