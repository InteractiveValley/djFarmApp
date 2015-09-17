# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(null=True, verbose_name=b'creado', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='modified',
            field=models.DateTimeField(null=True, verbose_name=b'actualizado', blank=True),
        ),
    ]
