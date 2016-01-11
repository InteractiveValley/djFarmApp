# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0015_auto_20151225_1342'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carrito', '0009_sale_notes'),
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
                ('user', models.ForeignKey(verbose_name=b'usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'recibo',
            },
        ),
    ]
