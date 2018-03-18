from django.core.signals import pre_save
from django.dispatch import receiver
from shop_order.models import OrderMain, OrderDetail
from django.db import F


@receiver(pre_save, sender=OrderMain)
def cancel_order_signal(sender, **kwargs):
    order = kwargs['instance']
    if order.is_pay is '-1':
        order_details = OrderDetail.objects.filter(order=order)
        for order_detail in order_details:
            order_detail.goods_info.stock = F('stock') + order_detail.count
            order_detail.save()
