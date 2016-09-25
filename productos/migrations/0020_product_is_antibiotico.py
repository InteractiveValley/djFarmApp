# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0019_product_date_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_antibiotico',
            field=models.BooleanField(default=False, verbose_name=b'Antibiotico'),
        ),
    ]
