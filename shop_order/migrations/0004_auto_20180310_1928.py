# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-10 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_order', '0003_auto_20180305_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermain',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='\u603b\u4ef7\u683c'),
        ),
    ]
