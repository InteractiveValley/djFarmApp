# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0012_sale_card_conekta'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsale',
            name='discount_inapam',
            field=models.DecimalField(default=0, verbose_name=b'descuento inapam', max_digits=10, decimal_places=2),
        ),
    ]
