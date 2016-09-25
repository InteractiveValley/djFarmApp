# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0023_auto_20160321_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='inapam',
            name='created',
            field=models.DateTimeField(null=True, verbose_name=b'creado', blank=True),
        ),
    ]
