# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0020_product_is_antibiotico'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cb',
            field=models.CharField(max_length=140, null=True, verbose_name=b'Codigo de barras', blank=True),
        ),
    ]
