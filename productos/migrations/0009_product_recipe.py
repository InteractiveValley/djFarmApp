# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_discount_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='recipe',
            field=models.IntegerField(default=1, verbose_name=b'receta', choices=[(1, b'No require receta'), (2, b'El repartidor te pedira que le muestres la receta'), (3, b'El repartidor te pedira y se quedara con la receta')]),
        ),
    ]
