# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0015_cardconekta'),
        ('carrito', '0011_auto_20151226_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='card_conekta',
            field=models.ForeignKey(verbose_name=b'tarjeta', blank=True, to='usuarios.CardConekta', null=True),
        ),
    ]
