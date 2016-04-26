# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0015_auto_20160424_2151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='type_recipe',
            new_name='type_receipt',
        ),
    ]
