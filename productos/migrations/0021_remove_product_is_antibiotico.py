# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0020_product_is_antibiotico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_antibiotico',
        ),
    ]
