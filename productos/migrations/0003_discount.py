# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_auto_20150916_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name=b'tipo', choices=[(b'precio', b'Por precio'), (b'porcentaje', b'Por porcentaje'), (b'cantidad', b'Por cantidad')])),
                ('price', models.DecimalField(default=0, verbose_name=b'precio', max_digits=10, decimal_places=2)),
                ('percentage', models.PositiveSmallIntegerField(default=0, verbose_name=b'porcentaje')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name=b'cantidad')),
                ('date_begins', models.DateField(auto_now=True, verbose_name=b'inicia')),
                ('date_ends', models.DateField(null=True, verbose_name=b'finaliza', blank=True)),
                ('products', models.ManyToManyField(related_name='discounts', to='productos.Product')),
            ],
        ),
    ]
