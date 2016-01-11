# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0015_auto_20151225_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='with_tax',
            field=models.BooleanField(default=True, verbose_name=b'con IVA'),
        ),
    ]
