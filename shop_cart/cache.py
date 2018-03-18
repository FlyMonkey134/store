# -*- coding:utf8 -*-

from utls.cache import BaseRedis

class ShopCartCache(BaseRedis):
    key = 'shop_cart_cache_{0}'

    def add_cart(self,session_id,gid,by_num):
        self.conn.hset(self.key.format(session_id),gid,by_num)

    def hlen(self,session_id):
        return self.conn.hlen(self.key.format(session_id))

    def hgetall(self,session_id):
        return self.conn.hgetall(self.key.format(session_id))

    def hdel(self,session_id,gid):
        return self.conn.hdel(self.key.format(session_id),gid)

    def hget(self,session_id,gid):
        return self.conn.hget(self.key.format(session_id),gid)
