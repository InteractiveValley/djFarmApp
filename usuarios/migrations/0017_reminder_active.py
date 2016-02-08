# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0016_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='active',
            field=models.BooleanField(default=True, verbose_name=b'activo'),
        ),
    ]
