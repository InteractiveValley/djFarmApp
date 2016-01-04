# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carrito', '0010_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsale',
            name='tax',
            field=models.DecimalField(default=0, verbose_name=b'IVA', max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='sale',
            name='vendor',
            field=models.ForeignKey(related_name='vendor', verbose_name=b'vendedor', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='user',
            field=models.ForeignKey(related_name='user', verbose_name=b'cliente', to=settings.AUTH_USER_MODEL),
        ),
    ]
