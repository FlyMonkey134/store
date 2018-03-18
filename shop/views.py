# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import render,reverse,redirect
from models import GoodsInfo,GoodsCategory
from django.core.paginator import Paginator
from cache import BrowseCache
from django.db.models import F
# Create your views here.

#商城主页视图
class Index(View):
    def get(self,request):
        goods_list = []
        categorys_list = GoodsCategory.objects.filter(status=0).all()
        for categorys in categorys_list:
            good_info = GoodsInfo.objects.filter(category=categorys).order_by('click_count')[:4]
            goods_list.append({
                'goods_categorys':categorys,
                'goods_info':good_info
            })
        return render(request,'shop/index.html',locals())

#商品分类
class CateGory(View):
    def get(self,request,cid):
        curr_page = int(request.GET.get('curr_page',1))
        curr_order = request.GET.get('curr_order','id')

        object_list = GoodsInfo.objects.filter(category_id=cid).order_by(curr_order)

        page = Paginator(object_list,5)
        p = page.page(curr_page)

        params = {'cid':cid}
        return render(request,'shop/list.html',locals())

#商品详情
class Detail(View):

    def get(self,request,cid):
        goodsinfo = GoodsInfo.objects.get(pk=cid)

        #保存浏览记录，如果登录则以用户名为键，否则使用IP地址为键
        if request.user.is_authenticated():
            BrowseCache().add_browse(request.user.id,goodsinfo.id)
        else:
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            BrowseCache().add_browse(ip,goodsinfo.id)

        # 点击量每次加1
        # 数据库原子操作，防止同时请求时会出现只请求到了一次
        GoodsInfo.objects.filter(click_count=F('click_count')+1)
        return render(request,'shop/detail.html',locals())