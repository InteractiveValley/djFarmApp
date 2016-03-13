# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0019_auto_20160206_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='title',
            field=models.CharField(default=b'', max_length=140, verbose_name=b'title'),
        ),
    ]
