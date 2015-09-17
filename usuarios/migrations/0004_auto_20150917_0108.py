# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20150916_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledorder',
            name='period',
            field=models.CharField(max_length=100, verbose_name=b'periodo', choices=[(b'por dia', b'Por dia'), (b'semanal', b'Semanal'), (b'mensual', b'Mensual')]),
        ),
    ]
