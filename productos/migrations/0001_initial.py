# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140, verbose_name=b'categoria')),
                ('image_require', models.ImageField(upload_to=b'categorias/require/', verbose_name=b'imagen require')),
                ('image_no_require', models.ImageField(upload_to=b'categorias/norequire/', verbose_name=b'imagen no require')),
            ],
            options={
                'verbose_name': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140, verbose_name=b'producto')),
                ('description', models.TextField(verbose_name=b'descripcion')),
                ('price', models.DecimalField(verbose_name=b'precio', max_digits=10, decimal_places=2)),
                ('require_prescription', models.BooleanField(verbose_name=b'require receta')),
                ('active', models.BooleanField(verbose_name=b'es activo')),
                ('category', models.ForeignKey(verbose_name=b'categoria', to='productos.Category')),
            ],
            options={
                'verbose_name': 'producto',
            },
        ),
    ]
