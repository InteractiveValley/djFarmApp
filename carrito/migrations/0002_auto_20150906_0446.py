# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productos', '0002_auto_20150906_0126'),
        ('carrito', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='enviar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='usuarios.Direction', null=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='product',
            field=models.ForeignKey(to='productos.Product'),
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(to='carrito.Venta'),
        ),
    ]
