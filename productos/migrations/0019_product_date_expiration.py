# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0018_auto_20160327_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_expiration',
            field=models.DateTimeField(null=True, verbose_name=b'Caducidad', blank=True),
        ),
    ]
