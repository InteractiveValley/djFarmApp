# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'verbose_name': 'descuento', 'verbose_name_plural': 'descuentos'},
        ),
        migrations.AlterField(
            model_name='discount',
            name='date_begins',
            field=models.DateField(null=True, verbose_name=b'inicia', blank=True),
        ),
    ]
