# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-25 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u5546\u54c1\u4ea7\u5730')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u5546\u54c1\u5206\u7c7b')),
                ('status', models.IntegerField(choices=[(0, '\u6b63\u5e38'), (1, '\u5220\u9664')], default=0, verbose_name='\u72b6\u6001')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u5546\u54c1\u540d\u79f0')),
                ('images', models.ImageField(upload_to='goods/%Y/%m/%d', verbose_name='\u56fe\u7247\u8def\u5f84')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u5546\u54c1\u4ef7\u683c')),
                ('click_count', models.IntegerField(default=0, verbose_name='\u5546\u54c1\u70b9\u51fb\u91cf')),
                ('unit', models.CharField(max_length=10, verbose_name='\u5546\u54c1\u5355\u4f4d')),
                ('status', models.IntegerField(choices=[(0, '\u6b63\u5e38'), (1, '\u5220\u9664')], default=0, verbose_name='\u5546\u54c1\u72b6\u6001')),
                ('description', models.TextField(verbose_name='\u5546\u54c1\u63cf\u8ff0')),
                ('stock', models.IntegerField(verbose_name='\u5546\u54c1\u5e93\u5b58')),
                ('detail', tinymce.models.HTMLField(verbose_name='\u5546\u54c1\u8be6\u60c5')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.GoodsArea', verbose_name='\u5546\u54c1\u4ea7\u5730')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.GoodsCategory', verbose_name='\u5546\u54c1\u5206\u7c7b')),
            ],
        ),
    ]
