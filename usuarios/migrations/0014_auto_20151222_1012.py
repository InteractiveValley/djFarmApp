# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0013_auto_20151222_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenphone',
            name='token',
            field=models.CharField(max_length=250, null=True, verbose_name=b'token', blank=True),
        ),
    ]
