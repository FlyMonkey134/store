# -*- coding:utf8 -*-

from .cache import ShopCartCache
from .models import ShopCart

def goods_num(request):

    my_session = request.COOKIES.get('my_session')
    shopcartcache = ShopCartCache()

    if request.user.is_authenticated():
        '''
            登陆时从redis中读取数据并放置数据库，同时从数据库中得到购物车已有的商品数量加以显示
            未登录则从redis的读取商品数量并加以显示
        '''

        cache_goods_num = shopcartcache.hgetall(my_session)

        if cache_goods_num:
            #如果redis中有数据，则将数据写入至数据库中，并清空redis中的数据
            for gid,buy_num in cache_goods_num.items():
                # hgetall得到的是一个字典
                shop_cart,is_create = ShopCart.objects.update_or_create(user=request.user, goodinfo_id=gid)
                shop_cart.buy_num = buy_num
                shop_cart.save()
                shopcartcache.hdel(my_session,gid)
        goods_num = ShopCart.objects.filter(user=request.user).count()

    else:
        goods_num = shopcartcache.hlen(my_session)

    return {
        'goods_num':goods_num
    }