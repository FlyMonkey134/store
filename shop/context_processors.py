# -*- coding:utf8 -*-

from shop.models import GoodsCategory
from shop.models import GoodsInfo


def categorys(request):
    categorys_list = GoodsCategory.objects.filter(status=0).all()
    return {'categorys_list': categorys_list}