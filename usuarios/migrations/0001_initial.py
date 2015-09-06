# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productos', '0002_auto_20150906_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('localidad', models.CharField(max_length=140)),
                ('calle', models.CharField(max_length=140)),
                ('num_interior', models.CharField(max_length=50)),
                ('num_exterior', models.CharField(max_length=50)),
                ('codigo_postal', models.CharField(max_length=10)),
                ('colonia', models.CharField(max_length=150)),
                ('delegacion_municipio', models.CharField(max_length=150)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoPeriodico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField()),
                ('periodo', models.CharField(max_length=100)),
                ('lunes', models.BooleanField()),
                ('martes', models.BooleanField()),
                ('miercoles', models.BooleanField()),
                ('jueves', models.BooleanField()),
                ('viernes', models.BooleanField()),
                ('sabado', models.BooleanField()),
                ('domingo', models.BooleanField()),
                ('proxima_entrega', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('producto', models.ForeignKey(to='productos.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pregunta', models.CharField(max_length=140)),
                ('respuesta', models.TextField()),
                ('orden', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cell', models.CharField(max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
