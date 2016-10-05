# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0024_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='shipping',
            field=models.DecimalField(default=0, verbose_name=b'envio', max_digits=10, decimal_places=2),
        ),
    ]
