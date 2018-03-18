# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserProFiles, DeliveryAddress


# Register your models here.


@admin.register(UserProFiles)
class UserProFilesAdmin(admin.ModelAdmin):
    verbose_name = u'用户'
    list_per_page = 20
    list_display = ['username', 'email', 'date_joined', 'last_login', 'delivertaddress']

    search_fields = ['username', 'email', ]
    def user_phone(self, obj):
        telphone = obj.delivertaddress
        print(telphone)
        return telphone


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'address', 'recipients', 'telphone', 'user']
    search_fields = ['recipients', 'telphone', 'user']