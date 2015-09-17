# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0004_auto_20150917_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailsale',
            name='image_recipe',
            field=models.ImageField(upload_to=b'detalleventa/recetas/', null=True, verbose_name=b'receta', blank=True),
        ),
    ]
