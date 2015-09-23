# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_auto_20150917_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConektaUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conekta_user', models.CharField(max_length=140, verbose_name=b'conekta')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'es_activo')),
                ('is_default', models.BooleanField(default=False, verbose_name=b'es_default')),
                ('created', models.DateTimeField(null=True, verbose_name=b'creado', blank=True)),
                ('modified', models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True)),
                ('user', models.ForeignKey(related_name='conektas', verbose_name=b'user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
