# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='created',
            field=models.DateTimeField(null=True, verbose_name=b'creado', blank=True),
        ),
        migrations.AlterField(
            model_name='direction',
            name='modified',
            field=models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True),
        ),
        migrations.AlterField(
            model_name='scheduledorder',
            name='created',
            field=models.DateTimeField(null=True, verbose_name=b'creado', blank=True),
        ),
        migrations.AlterField(
            model_name='scheduledorder',
            name='modified',
            field=models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True),
        ),
    ]
