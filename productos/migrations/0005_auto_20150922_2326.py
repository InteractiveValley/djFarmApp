# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_auto_20150917_0229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='products',
        ),
        migrations.AddField(
            model_name='discount',
            name='product',
            field=models.ForeignKey(related_name='discount', blank=True, to='productos.Product', null=True),
        ),
    ]
