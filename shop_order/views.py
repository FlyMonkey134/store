# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from .models import OrderMain, OrderDetail
from account.models import DeliveryAddress
from django.db import transaction
from django.db.models import F
from utls.error import StockException
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


# 购物车结算页面
class ShowOrder(LoginRequiredMixin, View):
    def get(self, request, oid):
        order_main = OrderMain.objects.get(pk=oid)
        address = DeliveryAddress.objects.filter(user=request.user).all()
        order_detail = OrderDetail.objects.filter(order=order_main).all()
        return render(request, 'shop_order/place_order.html', locals())

    def post(self, request, oid):
        # 购物车提交
        order_main = OrderMain.objects.get(pk=oid)
        order_detail = OrderDetail.objects.filter(order=order_main).all()
        address_id = request.POST.get('address_id')
        address = DeliveryAddress.objects.get(pk=address_id)
        try:
            with transaction.atomic():
                # 使用事务进行库存的删减，当其中一项出现错误时，则所有操作都将回原。
                # 如果库存不足则抛出异常，否则将数据库做原子操作，保证每次的数据
                # 都是数据库里最新的数据。
                for detail in order_detail:
                    if detail.count > detail.goods_info.stock:
                        raise StockException(u'%s库存不足' % detail.goods_info)
                    detail.goods_info.stock = F('stock') - detail.count
                    detail.goods_info.save()
                    order_main.total += detail.goods_total
                order_main.receiver = address
                order_main.is_pay = '1'
                order_main.total += 10
                order_main.save()
        except StockException:
            order_main.is_pay = '-1'
            order_main.save()
            message = u'%s,商品id=%s库存不足，订单已被自动取消'\
                % (detail.goods_info.name, detail.goods_info.id)
            return render(request, 'shop_order/message.html', locals())
        message = u'下单成功，请尽快前往支付。'
        return render(request, 'shop_order/message.html', locals())


# 取消订单视图，返回Json数据提供给前端
class CancelOrder(View):

    def get(self, request):
        data = {'code': 0}
        order_id = request.GET.get('order_id')
        print(order_id)
        order_main = OrderMain.objects.get(pk=order_id)
        # 用户不能修改自己以外的订单
        if order_main.user != request.user:
            return HttpResponseBadRequest()

        # 查看当前订单状态是否为1
        if order_main.is_pay == '1':
            order_main.is_pay = '-1'
            order_main.save()
        else:
            data['code'] = '1'
            data['message'] = u'订单取消失败'
        return JsonResponse(data)
