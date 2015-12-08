# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0013_receipt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image_no_require',
        ),
        migrations.RemoveField(
            model_name='category',
            name='image_require',
        ),
        migrations.RemoveField(
            model_name='category',
            name='image_require_show',
        ),
        migrations.AddField(
            model_name='category',
            name='image_category',
            field=models.ImageField(upload_to=b'categorias/', null=True, verbose_name=b'Imagen', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image_no_require',
            field=models.ImageField(upload_to=b'productos/norequire/', null=True, verbose_name=b'Sin receta', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image_require',
            field=models.ImageField(upload_to=b'productos/require/', null=True, verbose_name=b'Quedarse receta', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image_require_show',
            field=models.ImageField(upload_to=b'productos/require/', null=True, verbose_name=b'Mostrar receta', blank=True),
        ),
    ]
