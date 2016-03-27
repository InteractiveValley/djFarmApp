# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0017_category_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_enter',
            field=models.DateTimeField(null=True, verbose_name=b'Fecha entrada', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='date_out',
            field=models.DateTimeField(null=True, verbose_name=b'Fecha salida', blank=True),
        ),
    ]
