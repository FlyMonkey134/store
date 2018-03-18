# -*- coding:utf8 -*-

from django import forms


# 后台添加商品验证
class GoodsInfoForms(forms.ModelForm):
    name = forms.CharField(label=u'商品名称', max_length=30, min_length=4, required=True)
    images = forms.ImageField(label=u'商品图片', required=True)
    price = forms.DecimalField(label=u'商品价格', max_digits=10, required=True)
    click_count = forms.IntegerField(label=u'点击量')
    unit = forms.CharField(label=u'商品单位', max_length=10)
    description = forms.CharField(label=u'商品描述', required=True)
    stock = forms.IntegerField(label=u'商品库存', required=True)


