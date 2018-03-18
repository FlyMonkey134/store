# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .form import GoodsInfoForms
from .models import GoodsInfo,GoodsCategory, GoodsArea 




@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'unit', 'click_count', 'status', 'stock', ]
    list_per_page = 20
    search_fields = ['name']

    form = GoodsInfoForms