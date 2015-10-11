# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_auto_20151004_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(default=0, verbose_name=b'calificacion')),
                ('created', models.DateTimeField(null=True, verbose_name=b'creado', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='inapam',
            field=models.BooleanField(default=False, verbose_name=b'INAPAM'),
        ),
        migrations.AlterField(
            model_name='scheduledorder',
            name='days',
            field=models.PositiveIntegerField(default=1, verbose_name=b'dias'),
        ),
        migrations.AlterField(
            model_name='scheduledorder',
            name='product',
            field=models.ForeignKey(verbose_name=b'producto', to='productos.Product'),
        ),
        migrations.AlterField(
            model_name='scheduledorder',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name=b'cantidad'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(related_query_name=b'rating', related_name='ratings', verbose_name=b'usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
