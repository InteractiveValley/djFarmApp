# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20150916_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledorder',
            name='date_ends',
            field=models.DateField(null=True, verbose_name=b'finaliza', blank=True),
        ),
        migrations.AlterField(
            model_name='scheduledorder',
            name='date_next',
            field=models.DateField(null=True, verbose_name=b'proxima entrega', blank=True),
        ),
    ]
