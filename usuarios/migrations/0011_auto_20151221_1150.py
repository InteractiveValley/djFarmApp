# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0010_rating_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenPhone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=140, null=True, verbose_name=b'token', blank=True)),
                ('created', models.DateTimeField(null=True, verbose_name=b'creado', blank=True)),
                ('user', models.ForeignKey(related_query_name=b'tokenphones', related_name='tokenphones', verbose_name=b'usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='inapam',
            name='inapam',
            field=models.ImageField(upload_to=b'inapam/'),
        ),
    ]
