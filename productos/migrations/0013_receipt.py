# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0012_product_substances'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=0, verbose_name=b'recibido')),
                ('status', models.BooleanField(default=False, verbose_name=b'procesado')),
                ('created', models.DateTimeField(null=True, verbose_name=b'creado', blank=True)),
                ('modified', models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True)),
                ('product', models.ForeignKey(verbose_name=b'producto', to='productos.Product')),
            ],
            options={
                'verbose_name': 'recibo',
            },
        ),
    ]
