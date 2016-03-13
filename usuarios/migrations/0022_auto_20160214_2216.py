# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0021_auto_20160214_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledorder',
            name='card_conekta',
            field=models.ForeignKey(blank=True, to='usuarios.CardConekta', null=True),
        ),
        migrations.AddField(
            model_name='scheduledorder',
            name='direction',
            field=models.ForeignKey(blank=True, to='usuarios.Direction', null=True),
        ),
    ]
