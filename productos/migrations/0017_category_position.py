# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0016_product_with_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='position',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'posicion'),
        ),
    ]
