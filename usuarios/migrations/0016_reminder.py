# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0015_cardconekta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=140, verbose_name=b'mensaje')),
                ('time', models.TimeField(null=True, verbose_name=b'tiempo')),
                ('monday', models.BooleanField(default=False, verbose_name=b'lunes')),
                ('tuesday', models.BooleanField(default=False, verbose_name=b'martes')),
                ('wednesday', models.BooleanField(default=False, verbose_name=b'miercoles')),
                ('thursday', models.BooleanField(default=False, verbose_name=b'jueves')),
                ('friday', models.BooleanField(default=False, verbose_name=b'viernes')),
                ('saturday', models.BooleanField(default=False, verbose_name=b'sabado')),
                ('sunday', models.BooleanField(default=False, verbose_name=b'domingo')),
                ('user', models.ForeignKey(related_name='reminders', verbose_name=b'usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
