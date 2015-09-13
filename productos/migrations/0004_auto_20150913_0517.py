# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_auto_20150912_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image_no_require',
            field=models.ImageField(upload_to=b'categorias/norequire/', verbose_name=b'imagen no require'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image_require',
            field=models.ImageField(upload_to=b'categorias/require/', verbose_name=b'imagen require'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=140, verbose_name=b'categoria'),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(verbose_name=b'es activo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(verbose_name=b'categoria', to='productos.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name=b'descripcion'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=140, verbose_name=b'producto'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(verbose_name=b'precio', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='require_prescription',
            field=models.BooleanField(verbose_name=b'require receta'),
        ),
    ]
