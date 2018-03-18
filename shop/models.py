# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField

# Create your models here.


# 商品分类
class GoodsCategory(models.Model):
    STATUS = ((0, u'正常'), (1, u'删除'))

    name = models.CharField(max_length=20, verbose_name=u'商品分类')
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=u'状态')

    class Meta:
        verbose_name = u'商品分类'
        verbose_name_plural = u'商品分类'

    def __unicode__(self):
        return self.name


# 商品产地
class GoodsArea(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'商品产地')

    class Meta:
        verbose_name = '商品产地'
        verbose_name_plural = '商品产地'

    def __unicode__(self):
        return self.name


# 商品信息
class GoodsInfo(models.Model):
    STATUS = ((0, '正常'), (1, '删除'))

    name = models.CharField(max_length=30, verbose_name=u'商品名称')
    images = models.ImageField(upload_to='goods/%Y/%m/%d', verbose_name=u'图片路径')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'商品价格')
    click_count = models.IntegerField(default=0, verbose_name=u'商品点击量')
    unit = models.CharField(max_length=10, verbose_name=u'商品单位')
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=u'商品状态')
    description = models.TextField(verbose_name=u'商品描述')
    stock = models.IntegerField(verbose_name=u'商品库存')
    detail = HTMLField(verbose_name=u'商品详情')
    category = models.ForeignKey('GoodsCategory', verbose_name=u'商品分类')
    area = models.ForeignKey('GoodsArea', verbose_name=u'商品产地', null=True)

    class Meta:
        verbose_name = u'商品信息'
        verbose_name_plural = u'商品信息列表'

    def __unicode__(self):
        return self.name
