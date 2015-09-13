# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_auto_20150906_0126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'categoria'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'producto'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='is_active',
            new_name='active',
        ),
    ]
