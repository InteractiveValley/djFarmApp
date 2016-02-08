# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0017_reminder_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardconekta',
            name='allow_charges',
            field=models.BooleanField(default=False, verbose_name=b'permite cargos'),
        ),
        migrations.AddField(
            model_name='cardconekta',
            name='allow_payouts',
            field=models.BooleanField(default=False, verbose_name=b'permite pagos'),
        ),
        migrations.AddField(
            model_name='cardconekta',
            name='bank_name',
            field=models.CharField(default=b'', max_length=140, verbose_name=b'institucion bancaria'),
        ),
        migrations.AddField(
            model_name='cardconekta',
            name='type',
            field=models.CharField(default=b'Credit', max_length=140, verbose_name=b'tipo tarjeta'),
        ),
    ]
