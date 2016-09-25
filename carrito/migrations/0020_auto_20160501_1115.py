# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0019_auto_20160428_0515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailsend',
            name='detail',
        ),
        migrations.AddField(
            model_name='detailsale',
            name='quantity_shipping',
            field=models.IntegerField(default=0, verbose_name=b'cantidad enviada'),
        ),
        migrations.AddField(
            model_name='detailsale',
            name='with_shipping',
            field=models.BooleanField(default=False, verbose_name=b'con envio'),
        ),
        migrations.AddField(
            model_name='detailsend',
            name='date_expiration',
            field=models.DateField(null=True, verbose_name=b'expira', blank=True),
        ),
        migrations.AddField(
            model_name='detailsend',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name=b'recibido'),
        ),
        migrations.AddField(
            model_name='detailsend',
            name='status',
            field=models.BooleanField(default=False, verbose_name=b'procesado'),
        ),
        migrations.AddField(
            model_name='detailsend',
            name='type_receipt',
            field=models.IntegerField(default=2, verbose_name=b'Tipo de trasaccion'),
        ),
        migrations.AlterField(
            model_name='detailsend',
            name='detail_sale',
            field=models.ForeignKey(related_name='detail_sends', verbose_name=b'linea', to='carrito.DetailSale'),
        ),
        migrations.AlterField(
            model_name='detailsend',
            name='receipt',
            field=models.ForeignKey(related_name='detail_sends', verbose_name=b'recibo asociado', to='carrito.Receipt'),
        ),
    ]
