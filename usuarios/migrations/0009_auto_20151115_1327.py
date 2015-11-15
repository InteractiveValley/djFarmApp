# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_auto_20151010_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inapam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inapam', models.ImageField(upload_to=b'/inapam')),
                ('active', models.BooleanField(default=False, verbose_name=b'Autorizado')),
                ('user', models.ForeignKey(related_query_name=b'images_inapam', related_name='images_inapam', verbose_name=b'usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='direction',
            name='active',
            field=models.BooleanField(default=True, verbose_name=b'activa'),
        ),
    ]
