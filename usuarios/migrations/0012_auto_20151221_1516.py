# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0011_auto_20151221_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenphone',
            name='user',
            field=models.ForeignKey(verbose_name=b'usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
