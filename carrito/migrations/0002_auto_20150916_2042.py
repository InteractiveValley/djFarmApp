# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productos', '0001_initial'),
        ('carrito', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name=b'precio', max_digits=10, decimal_places=2)),
                ('quantity', models.IntegerField(verbose_name=b'cantidad')),
                ('image_recipe', models.ImageField(upload_to=b'detalleventa/recetas/', verbose_name=b'receta')),
                ('validate', models.BooleanField(default=False, verbose_name=b'validado')),
                ('product', models.ForeignKey(to='productos.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField(default=False, verbose_name=b'aprovado')),
                ('scheduled_order', models.BooleanField(default=False, verbose_name=b'pedido programado')),
                ('delivered', models.BooleanField(default=False, verbose_name=b'entregado')),
                ('created', models.DateTimeField(verbose_name=b'creado')),
                ('modified', models.DateTimeField(verbose_name=b'actualizado')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='usuarios.Direction', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='detalleventa',
            name='product',
        ),
        migrations.RemoveField(
            model_name='detalleventa',
            name='venta',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='enviar',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='user',
        ),
        migrations.DeleteModel(
            name='DetalleVenta',
        ),
        migrations.DeleteModel(
            name='Venta',
        ),
        migrations.AddField(
            model_name='detailsale',
            name='sale',
            field=models.ForeignKey(to='carrito.Sale'),
        ),
    ]
