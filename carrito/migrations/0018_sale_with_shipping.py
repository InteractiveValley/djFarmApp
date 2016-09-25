# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0017_auto_20160427_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='with_shipping',
            field=models.BooleanField(default=False, verbose_name=b'con envio'),
        ),
    ]
