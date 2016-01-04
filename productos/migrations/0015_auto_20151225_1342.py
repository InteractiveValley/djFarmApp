# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0014_auto_20151208_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name=b'laboratorio')),
            ],
            options={
                'verbose_name': 'laboratorio',
                'verbose_name_plural': 'laboratorios',
            },
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='product',
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
        migrations.AddField(
            model_name='product',
            name='laboratory',
            field=models.ForeignKey(verbose_name=b'laboratorio', blank=True, to='productos.Laboratory', null=True),
        ),
    ]
