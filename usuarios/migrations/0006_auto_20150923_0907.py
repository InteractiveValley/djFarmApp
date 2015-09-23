# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_conektauser'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='lat',
            field=models.CharField(max_length=100, null=True, verbose_name=b'latitude', blank=True),
        ),
        migrations.AddField(
            model_name='direction',
            name='lng',
            field=models.CharField(max_length=100, null=True, verbose_name=b'longitude', blank=True),
        ),
    ]
