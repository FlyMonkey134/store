# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-05 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermain',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.DeliveryAddress', verbose_name='\u6536\u8d27\u8be6\u60c5'),
        ),
    ]
