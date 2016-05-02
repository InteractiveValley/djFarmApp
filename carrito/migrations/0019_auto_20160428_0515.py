# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0018_sale_with_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailsend',
            name='send',
            field=models.ForeignKey(related_name='detail_sends', verbose_name=b'envio', to='carrito.Send'),
        ),
    ]
