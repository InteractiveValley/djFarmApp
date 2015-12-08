# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0008_auto_20151004_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='notes',
            field=models.TextField(null=True, verbose_name=b'Notas/Comentarios', blank=True),
        ),
    ]
