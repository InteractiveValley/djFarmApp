# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0002_auto_20150916_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='created',
            field=models.DateTimeField(null=True, verbose_name=b'creado', blank=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='modified',
            field=models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True),
        ),
    ]
