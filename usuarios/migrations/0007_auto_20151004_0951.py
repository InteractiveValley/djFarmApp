# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_auto_20150923_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='colony',
            field=models.CharField(max_length=150, null=True, verbose_name=b'colonia', blank=True),
        ),
        migrations.AlterField(
            model_name='direction',
            name='delegation_municipaly',
            field=models.CharField(max_length=150, null=True, verbose_name=b'delegacion o municipio', blank=True),
        ),
        migrations.AlterField(
            model_name='direction',
            name='postal_code',
            field=models.CharField(max_length=10, null=True, verbose_name=b'codigo postal', blank=True),
        ),
    ]
