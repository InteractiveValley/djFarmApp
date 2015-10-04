# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0009_product_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_require_show',
            field=models.ImageField(upload_to=b'categorias/require/', null=True, verbose_name=b'Mostrar receta', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='image_no_require',
            field=models.ImageField(upload_to=b'categorias/norequire/', null=True, verbose_name=b'Sin receta', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='image_require',
            field=models.ImageField(upload_to=b'categorias/require/', null=True, verbose_name=b'Quedarse receta', blank=True),
        ),
    ]
