# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-17 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_mailrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, '\u7537'), (1, '\u5973')], default=0, verbose_name='\u6027\u522b'),
            preserve_default=False,
        ),
    ]
