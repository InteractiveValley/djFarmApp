# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0022_auto_20160214_2216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inapam',
            old_name='inapam',
            new_name='image',
        ),
        migrations.AddField(
            model_name='inapam',
            name='vendor',
            field=models.ForeignKey(related_query_name=b'inapam_vendor', related_name='inapam_vendor', verbose_name=b'vendor', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='cardconekta',
            name='bank_name',
            field=models.CharField(default=b'', max_length=140, null=True, verbose_name=b'institucion bancaria', blank=True),
        ),
    ]
