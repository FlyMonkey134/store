# -*- coding:utf8 -*-
from shop.models import GoodsInfo
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from urllib import urlencode
import urllib2
from django.utils.safestring import mark_safe


register = template.Library()


# 新品推荐
@register.inclusion_tag('shop/refferral_good.html')
def refferral_goods(cid=None):
    if cid:
        refferral_goods = GoodsInfo.objects.filter(category_id=cid).order_by('-id')[:2]
    else:
        refferral_goods = GoodsInfo.objects.order_by('-id')[:2]
    return {
        'refferral_goods': refferral_goods,
        'MEDIA_URL': settings.MEDIA_URL
    }


# 分页
@register.simple_tag
def smart_page(curr_url, page_obj, url_name, request_url, page_name='curr_page', kwargs={}, *args):
    '''

    :param curr_url: 当前页码
    :param page_obj: 一个page对象
    :param url_name: 当前URL
    :param request_url: 请求的URL
    :param page_name: 页码
    :param args: 可能需要传递的参数
    :param kwargs: 可能需要传递的参数
    :return: 返回最终的HTML标签

    此函数首先获取当前URL，将当前的URL传递给page，获得一个分页对象。然后
    根据是否有上下页而现实不同的标签。最终返回一个完整的HTML代码。

    **注：
        这里不能直接返回字符串，若直接返回字符串则不换转换为HTML代码，必须使用mark_safe将字符串
        转换为对应的HTML代码。

    '''
    str_tag = '<div class="pagenation">'
    # 此字典用来存储URL参数
    params = {}
    # 获取URL(不带参数)
    url = reverse(url_name, args=args, kwargs=kwargs)
    p = page_obj.page(curr_url)

    # 设置每页最多显示五页
    max_page = 5
    page_list = [page for page in page_obj.page_range]
    center_index = max_page / 2

    # 获取当前页面所在page的位置
    page_url = page_list.index(curr_url)

    request_url = urllib2.unquote(request_url.encode('utf-8'))
    # 当前页面数量大于偏移量时，将页面
    if page_url > center_index:
        page_list = page_list[page_url - center_index:]
    # 设置排序
    try:
        for param in request_url.split("?")[-1].split("&"):
            params[param.split('=')[0]] = param.split('=')[1]
    except:
        request_url += '?curr_order=id'

    # 首页
    params[page_name] = page_obj.page_range[0]
    curl_url = '%s?%s' % (url, urlencode(params))
    print(curl_url)
    str_tag += u'<a href="%s">首页</a>' % curl_url

    # 上一页
    if p.has_previous():
        params[page_name] = curr_url - 1
        curl_url = '%s?%s' % (url, urlencode(params))
        str_tag += u'<a href="%s">上一页</a>' % curl_url

    # 添加页码
    for i, p_id in enumerate(page_list):
        params[page_name] = p_id
        curl_url = '%s?%s' % (url, urlencode(params))

        if i >= max_page:
            break

        # 判断是否为当前页面
        if p_id == curr_url:
            str_tag += u'<a href="%s" class="active">%s</a>' % (curl_url, p_id)
        else:
            str_tag += u'<a href="%s">%s</a>' % (curl_url, p_id)

    # 下一页
    if p.has_next():
        params[page_name] = curr_url + 1
        curl_url = '%s?%s' % (url, urlencode(params))
        str_tag += u'<a href="%s">下一页</a>' % curl_url

    # 尾页
    params[page_name] = page_obj.page_range[-1]
    curl_url = '%s?%s' % (url, urlencode(params))
    str_tag += u'<a href="%s">尾页</a>' % curl_url

    str_tag += '</div>'
    return mark_safe(str_tag)
