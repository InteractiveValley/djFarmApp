# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0007_auto_20151001_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='charge_conekta',
            field=models.CharField(default=b'', max_length=140, null=True, verbose_name=b'Cargo Id Conekta', blank=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='status',
            field=models.IntegerField(default=0, verbose_name=b'Estatus', choices=[(5, b'Pagado'), (0, b'Incompleto'), (4, b'Entregado'), (1, b'Completo'), (3, b'Rechazado'), (6, b'No pagado'), (2, b'Aprobado')]),
        ),
    ]
