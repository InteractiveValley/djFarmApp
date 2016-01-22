# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0014_auto_20151222_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardConekta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card', models.CharField(max_length=100, verbose_name=b'card')),
                ('name', models.CharField(max_length=140, verbose_name=b'name')),
                ('brand', models.CharField(max_length=140, verbose_name=b'brand')),
                ('last4', models.CharField(max_length=140, verbose_name=b'last4')),
                ('active', models.BooleanField(default=True, verbose_name=b'active')),
                ('exp_year', models.CharField(max_length=4, verbose_name=b'exp year')),
                ('exp_month', models.CharField(max_length=2, verbose_name=b'exp month')),
                ('created', models.DateTimeField(null=True, verbose_name=b'creado', blank=True)),
                ('user', models.ForeignKey(related_name='cards', verbose_name=b'usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
