# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carrito', '0016_auto_20160425_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailSend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, verbose_name=b'creado', blank=True)),
                ('modified', models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True)),
                ('detail', models.ForeignKey(related_name='detail', verbose_name=b'salida asociada', to='carrito.Receipt')),
                ('detail_sale', models.ForeignKey(verbose_name=b'linea', to='carrito.DetailSale')),
                ('receipt', models.ForeignKey(related_name='receipt', verbose_name=b'recibo asociado', to='carrito.Receipt')),
            ],
        ),
        migrations.CreateModel(
            name='Send',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=False, verbose_name=b'Enviado')),
                ('created', models.DateTimeField(null=True, verbose_name=b'creado', blank=True)),
                ('modified', models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True)),
                ('sale', models.ForeignKey(verbose_name=b'venta', to='carrito.Sale')),
                ('vendor', models.ForeignKey(verbose_name=b'vendedor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='detailsend',
            name='send',
            field=models.ForeignKey(verbose_name=b'envio', to='carrito.Send'),
        ),
    ]
