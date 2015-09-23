# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0007_auto_20150922_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='short_name',
            field=models.CharField(default=b'-10%', max_length=20, null=True, verbose_name=b'etiqueta', blank=True),
        ),
    ]
