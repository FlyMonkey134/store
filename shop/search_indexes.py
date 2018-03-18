# -*- coding: utf-8 -*-

from haystack import indexes
from shop.models import GoodsInfo


class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    # 固定写法，所有定义的属性中，只有一个document=True
    text = indexes.CharField(document=True, use_template=True)

    # 关联的Model
    def get_model(self):
        return GoodsInfo

    # 更新索引时需要查询的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
