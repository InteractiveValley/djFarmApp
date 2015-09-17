# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('cell', models.CharField(max_length=50)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=140, verbose_name=b'localidad')),
                ('street', models.CharField(max_length=140, verbose_name=b'calle')),
                ('interior_number', models.CharField(max_length=50, null=True, verbose_name=b'numero interior', blank=True)),
                ('exterior_number', models.CharField(max_length=50, null=True, verbose_name=b'numero exterior', blank=True)),
                ('postal_code', models.CharField(max_length=10, verbose_name=b'codigo postal')),
                ('colony', models.CharField(max_length=150, verbose_name=b'colonia')),
                ('delegation_municipaly', models.CharField(max_length=150, verbose_name=b'delegacion o municipio')),
                ('created', models.DateTimeField(verbose_name=b'creado')),
                ('modified', models.DateTimeField(verbose_name=b'actualizado')),
                ('user', models.ForeignKey(related_name='directions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'direccion',
                'verbose_name_plural': 'direcciones',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=140, verbose_name=b'pregunta')),
                ('ask', models.TextField(verbose_name=b'respuesta')),
                ('order', models.IntegerField(verbose_name=b'orden')),
            ],
            options={
                'verbose_name': 'pregunta',
                'verbose_name_plural': 'preguntas',
            },
        ),
        migrations.CreateModel(
            name='ScheduledOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(verbose_name=b'cantidad')),
                ('period', models.CharField(max_length=100, verbose_name=b'periodo', choices=[(1, b'Por dia'), (2, b'Semanal'), (3, b'Mensual')])),
                ('days', models.PositiveIntegerField(verbose_name=b'dias')),
                ('times', models.IntegerField(default=0, verbose_name=b'veces')),
                ('date_next', models.DateTimeField(null=True, verbose_name=b'proxima entrega', blank=True)),
                ('date_ends', models.DateTimeField(null=True, verbose_name=b'finaliza', blank=True)),
                ('created', models.DateTimeField(verbose_name=b'creado')),
                ('modified', models.DateTimeField(verbose_name=b'actualizado')),
                ('canceled_for_user', models.BooleanField(default=False, verbose_name=b'cancelado por usuario')),
                ('canceled_for_system', models.BooleanField(default=False, verbose_name=b'finalizacion')),
                ('product', models.ForeignKey(to='productos.Product')),
                ('user', models.ForeignKey(related_name='schedules_orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'pedido programado',
                'verbose_name_plural': 'pedidos programados',
            },
        ),
    ]
