# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProFiles(AbstractUser):
    GENDER = ((0, '男'), (1,'女'))
    gender = models.SmallIntegerField(u'性别', choices=GENDER, default=None, null=True)

    delivertaddress = models.ForeignKey('DeliveryAddress',
                                        related_name='user_delivertaddress', null=True, default=None)

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户列表'


class MailRecord(models.Model):
    EMAIL_TYPE = ((0,u'激活'),(1,u'修改密码'))
    user = models.ForeignKey(UserProFiles)
    code = models.CharField(u'验证码',max_length=40)
    email = models.SmallIntegerField(choices=EMAIL_TYPE)
    create_time = models.TimeField(u'创建时间',auto_now=True)
    
    class Meta:
        verbose_name = u'邮箱验证'
        verbose_name_plural = u'邮箱验证列表'

class DeliveryAddress(models.Model):
    recipients = models.CharField(u'收件人',max_length=20)
    telphone = models.CharField(u'联系电话',max_length=11)
    city = models.CharField(u'城市',max_length=20)
    address = models.CharField(u'地址',max_length=50)
    user = models.ForeignKey('UserProFiles',related_name='user_deliveryaddress')

    class Meta:
        verbose_name = u'收货地址'
        verbose_name_plural = u'收货地址列表'

    def __unicode__(self):
        return self.city + self.address
