# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from shop.models import GoodsInfo
from account.models import UserProFiles
# Create your models here.

class ShopCart(models.Model):
    user = models.ForeignKey(UserProFiles)
    goodinfo = models.ForeignKey(GoodsInfo)
    create_time = models.DateTimeField(auto_now=True)
    buy_num = models.IntegerField(u'购买数量',default=0)

    class Meta:
        unique_together = ('user','goodinfo')