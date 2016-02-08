# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0018_auto_20160206_1302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardconekta',
            old_name='allow_charges',
            new_name='allows_charges',
        ),
        migrations.RenameField(
            model_name='cardconekta',
            old_name='allow_payouts',
            new_name='allows_payouts',
        ),
    ]
