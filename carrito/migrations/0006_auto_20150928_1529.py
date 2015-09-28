# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0005_auto_20150917_0406'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_recipe', models.ImageField(upload_to=b'recetas/', null=True, verbose_name=b'receta', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='detailsale',
            name='image_recipe',
        ),
        migrations.RemoveField(
            model_name='detailsale',
            name='validate',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='approved',
        ),
        migrations.AddField(
            model_name='sale',
            name='status',
            field=models.IntegerField(default=0, verbose_name=b'Estatus', choices=[(3, b'Rechazado'), (1, b'Completo'), (4, b'Entregado'), (0, b'Incompleto'), (2, b'Aprobado')]),
        ),
        migrations.AddField(
            model_name='imagesale',
            name='sale',
            field=models.ForeignKey(related_name='images', to='carrito.Sale'),
        ),
    ]
