# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from account.models import UserProFiles, DeliveryAddress
from shop.models import GoodsInfo


# Create your models here.


# 生成订单
class OrderMain(models.Model):
    order_status = (
        ('-1', '取消'),
        ('0', '创建'),
        ('1', '未支付'),
        ('2', '已支付'),
        ('3', '代发货'),
        ('4', '已发货')
    )
    
    uuid = models.CharField(max_length=50, unique=True, verbose_name=u'订单编号')
    order_time = models.DateTimeField(auto_now_add=True, verbose_name=u'订单提交时间')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name=u'付款时间')
    user = models.ForeignKey(UserProFiles, verbose_name=u'购买用户')
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=u'总价格')
    is_pay = models.CharField(max_length=5, choices=order_status, default='0', verbose_name=u'订单状态')
    receiver = models.ForeignKey(DeliveryAddress, null=True, verbose_name=u'收货详情')
    class Meta:
        verbose_name = u'订单中心'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

    def __str__(self):
        return str(self.user)


# 订单详情信息
class OrderDetail(models.Model):
    order = models.ForeignKey(OrderMain, verbose_name=u'订单中心')
    goods_info = models.ForeignKey(GoodsInfo, verbose_name=u'商品')
    goods_price = models.DecimalField(max_digits=10, null=True, decimal_places=2, verbose_name=u'商品价格')
    goods_total = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name=u'商品总价')
    count = models.IntegerField(verbose_name=u'购买商品数量')

    class Meta:
        verbose_name=u'订单详情'
        verbose_name_plural = verbose_name
        ordering =('-id',)

    def __str__(self):
        return str(self.order) + str(self.goods_info)
