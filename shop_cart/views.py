# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import redirect_to_login
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from cache import ShopCartCache
from .models import ShopCart
from shop.models import GoodsInfo
from shop_order.models import OrderMain, OrderDetail
import uuid
from utls.error import StockException

# Create your views here.


# 添加购物车
class AddCart(View):

    def get(self, request, gid):
        buy_num = request.GET.get('buy_num')

        '''
            如果登录则直接从数据库中获取商品，未登录则从缓存中获取
        '''
        if request.user.is_authenticated():
            shop_cart, is_create = ShopCart.objects.update_or_create(user=request.user, goodinfo_id=gid)
            shop_cart.buy_num = buy_num
            shop_cart.save()
            goods_num = ShopCart.objects.filter(user=request.user).count()
        else:
            session_id = request.COOKIES.get('my_session')
            shop_cart_cache = ShopCartCache()
            shop_cart_cache.add_cart(session_id, gid, buy_num)
            goods_num = shop_cart_cache.hlen(session_id)

        return JsonResponse({
            'code': 0,
            'goods_num': goods_num
        })


# 购物车详情页面
class ShowShopCart(View):
    def get(self, request):
        # 如果用户登录，则从数据库中加载购物车商品信息，否则从redis中获取
        my_session = request.COOKIES.get('my_session')
        shop_cart_cache = ShopCartCache()

        if request.user.is_authenticated():
            cart_info = ShopCart.objects.filter(user=request.user)
        else:
            # 从redis中加载购物车商品
            cart_info = []
            data = shop_cart_cache.hgetall(my_session)

            for gid, buy_num in data.items():
                cart_info.append({
                    'goodinfo': GoodsInfo.objects.get(pk=gid),
                    'buy_num': buy_num
                })
        return render(request, 'shop_cart/cart.html', locals())

    def post(self, request):
        # 当点击提交时，判断用户是否登录，如果没有则跳转至登录页面
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())

        cart_by_goods_ids = request.POST.getlist('cart_by_goods_id')
        with transaction.atomic():
            # 数据库事务，其中有任何一项出现问题都不会讲之前的数据保存至数据库
            # 通过获取购物车商品的id，返回一个包含ShopCart对象的字典
            shop_cart_dict = ShopCart.objects.in_bulk(id_list=cart_by_goods_ids)
            order_main = OrderMain(uuid=uuid.uuid4(), user=request.user, total=0)
            order_main.is_pay = '1'
            order_main.save()
            # 循环遍历购物车里的商品，并将数据添加至订单详情中。
            for shop_cart in shop_cart_dict.values():
                order_detail = OrderDetail()
                order_detail.order = order_main
                order_detail.goods_info = shop_cart.goodinfo
                order_detail.price = shop_cart.goodinfo.price
                order_detail.count = shop_cart.buy_num
                if shop_cart.buy_num > shop_cart.goodinfo.stock:
                    raise StockException(u'库存不足')
                order_detail.goods_total = float(shop_cart.goodinfo.price * shop_cart.buy_num)
                order_detail.save()
                ShopCart.objects.get(pk=shop_cart.id).delete()
        return redirect(reverse('show_order:show_order', kwargs={'oid': order_main.id}))


# 删除购物车商品
class DelShopCart(View):
    def get(self, request, gid):
        # 删除购物车商品
        # 如果用户登录，则将数据库的中的数据删除并返回状态码给前端
        # 如果用户未登录则将redis中的数据删除，并返回状态码给前端
        print(gid)
        if request.user.is_authenticated():
            ShopCart.objects.filter(user=request.user, goodinfo_id=gid).delete()

        else:
            my_session = request.COOKIES.get('my_session')
            shop_cart_cache = ShopCartCache()
            shop_cart_cache.hdel(my_session, gid)

        return JsonResponse({
            'code': 0
        })


# 购物车结算数量
class UpdateCart(View):

    def get(self, request, gid):
        data = {'code': 0}
        buy_num = int(request.GET.get('buy_num'))
        print(buy_num)
        if buy_num:
            goods_info = GoodsInfo.objects.get(pk=gid)
            if buy_num > goods_info.stock:
                data['code'] = 1
                data['stock'] = goods_info.stock
        if data['code'] == 0:
            if request.user.is_authenticated():
                ShopCart.objects.filter(pk=gid).update(buy_num=buy_num)
            else:
                my_session = request.COOKIES.get('my_session')
                shop_cart_cache = ShopCartCache()
                shop_cart_cache.add_cart(my_session, gid, buy_num)
            data['buy_num'] = buy_num
        return JsonResponse(data)
