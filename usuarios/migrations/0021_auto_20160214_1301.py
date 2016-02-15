# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0020_reminder_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=140, verbose_name=b'titulo')),
                ('message', models.CharField(max_length=255, verbose_name=b'mensaje')),
            ],
        ),
        migrations.AddField(
            model_name='tokenphone',
            name='active',
            field=models.BooleanField(default=True, verbose_name=b'activo'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='token_phone',
            field=models.ForeignKey(related_name='notifications', verbose_name=b'token_phone', to='usuarios.TokenPhone'),
        ),
    ]
