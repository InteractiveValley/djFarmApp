# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0012_auto_20151221_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenphone',
            name='user',
            field=models.ForeignKey(related_name='token_phone', verbose_name=b'usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
