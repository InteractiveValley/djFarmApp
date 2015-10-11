# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0011_auto_20151004_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='substances',
            field=models.CharField(default=b'', max_length=140, verbose_name=b'sustancia activa'),
        ),
    ]
