# -*- coding:utf8 -*-
from utls.cache import BaseRedis


class BrowseCache(BaseRedis):
    key = 'user_browse_cache_key_{}'

    def add_browse(self,key_name,gid):
        self.conn.rpush(self.key.format(key_name), gid)

    def lrange_browse(self,key_name):
        return self.conn.lrange(self.key.format(key_name),0,4)