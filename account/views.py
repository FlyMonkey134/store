# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views import View
from form import RegisterFrom, LoginForm, UserCenterSiteFrom
from models import UserProFiles, MailRecord, DeliveryAddress
from django.contrib.auth.hashers import make_password, check_password
from utls.email import register_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.cache import BrowseCache
from shop.models import GoodsInfo
from shop_order.models import OrderMain, OrderDetail
from django.core.paginator import Paginator

# Create your views here.


# 注册视图
class Register(View):
    def get(self, request):
        return render(request, 'account/register.html')

    def post(self, request):
        """
            获取对应的表单数据，然后从数据库查询对应的用户名，如果存在则返回消息到前端，
            如果不存在则创建用户。
        """
        register_form = RegisterFrom(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            user = UserProFiles.objects.filter(username=username).first()

            if not user:
                user = UserProFiles()
                user.username = register_form.cleaned_data['username']
                user.password = make_password(password=register_form.cleaned_data['password2'])
                user.email = register_form.cleaned_data['email']
                user.is_active = 0
                user.gender = 0
                user.save()
                register_mail(user)
                return render(request, 'account/send_success.html', locals())

            else:
                username = register_form.cleaned_data['username']
                count = UserProFiles.objects.filter(username=username).count()
                err_allow = u'用户名已存在'

        return render(request, 'account/register.html', locals())


# 登录视图
class Login(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(**login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('shop:index'), locals())
            else:
                err = u'用户名或密码错误'
                return render(request, 'account/login.html', locals())

        return render(request, 'account/login.html', locals())


# 查看用户名是否存在
class CheckUsername(View):
    def get(self, request):
        username = request.GET.get('username')
        count = UserProFiles.objects.filter(username=username).count()
        return JsonResponse({'count': count})


# 用户认证
class Activation(View):
    def get(self, request):
        code = request.GET.get('code')
        email = MailRecord.objects.filter(code=code).first()

        if email:
            email.user.is_active = True
            email.user.save()
            return redirect(reverse('account:login'), locals())
        else:
            return render(request, 'account/register.html', locals())


# 注销视图
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('shop:index'))


# 密码修改视图
class ChangePassWord(View):
    def get(self, request):
        return render(request, 'account/reset_password.html')

    def post(self, request):
        user_password = UserProFiles()
        # 获取原密码
        old_password = request.POST.get('password')
        # 获取原密码密文
        ciphertext = make_password(old_password)

        chk_password = check_password(old_password, ciphertext)
        print(chk_password)
        if chk_password:
            # 分析明文与密文查看是否与数据库的匹配
            hash_password = UserProFiles.objects.filter(password=ciphertext).first()
            print(hash_password)
            if hash_password:
                password2 = request.POST.get('password2')
                print(password2)
                user_password.objects.filter(password=hash_password).update(password=password2)
                user_password.save()
                return redirect(reverse('account:login'))
            else:
                print(u'修改失败哦')
                return render(request, 'account/reset_password.html')


# 用户个人中心视图
class UserCenterInfo(LoginRequiredMixin, View):

    def get(self, request):
        # 从缓存中读取浏览记录
        gids = BrowseCache().lrange_browse(request.user.id)
        goods_info_list = GoodsInfo.objects.in_bulk(id_list=gids)
        goods_info_list = goods_info_list.values()
        return render(request, 'account/user_center_info.html', locals())


# 我的订单视图
class UserCenterOrder(LoginRequiredMixin, View):
    def get(self, request):
        curr_page = int(request.GET.get('curr_page', 1))
        items = []
        order_main = OrderMain.objects.filter(user=request.user).all()
        page = Paginator(order_main, 3)
        p = page.page(curr_page)
        for order in p.object_list:
            order_detail = OrderDetail.objects.filter(order=order).all()
            items.append(
                {
                    'order_main': order,
                    'order_details': order_detail
                }
            )
        return render(request, 'account/user_center_order.html', locals())


# 添加收货地址
class UserCenterSite(LoginRequiredMixin, View):

    def get(self, request):
        receiver_infos = DeliveryAddress.objects.all()
        return render(request, 'account/user_center_site.html', locals())

    def post(self, request):
        # 实例化表单
        recipients_form = UserCenterSiteFrom(request.POST)
        if recipients_form.is_valid():
            recipients_model = DeliveryAddress(**recipients_form.cleaned_data)
            recipients_model.user = request.user
            recipients_model.save()
            return JsonResponse({'status': 0})
        else:
            return JsonResponse({'status': 1, 'errors': recipients_form.errors})


# 设置默认地址
class UserCenterSetSite(LoginRequiredMixin, View):
    def get(self, request):
        data_id = request.GET.get('data_id')
        print(data_id)
        request.user.delivertaddress_id = data_id
        request.user.save()

        return JsonResponse({'status': 0,
                             'recipients': request.user.delivertaddress.recipients,
                             'telphone': request.user.delivertaddress.telphone,
                             'city': request.user.delivertaddress.city,
                             'address': request.user.delivertaddress.address,
                             })


# 删除地址
class UserCenterDelSite(LoginRequiredMixin, View):
    def get(self, request):
        is_default = 1
        data_id = int(request.GET.get('data_id'))
        if request.user.delivertaddress.id == data_id:
            request.user.delivertaddress = None
            request.user.save()
            is_default = 0

        DeliveryAddress.objects.filter(id=data_id).delete()

        return JsonResponse({'status': 0, 'is_default': is_default})


# 编辑收货地址
class UserEditAddress(LoginRequiredMixin, View):
    def get(self, request):
        data_id = request.GET.get('data_id')
        old_addrs = DeliveryAddress.objects.get(pk=data_id)
        return JsonResponse({'status': 1,
                             'recipients': old_addrs.recipients,
                             'city': old_addrs.city,
                             'telphone': old_addrs.telphone,
                             'address': old_addrs.address
                             })


# 编辑当前收货地址
class UserEditSubmit(LoginRequiredMixin, View):
    def post(self, request):
        user_edit_addrs_form = UserCenterSiteFrom(request.POST)
        data_id = request.POST.get('data_id')
        res = {
            'status': 0
        }
        if user_edit_addrs_form.is_valid():
            # 将表单内容赋值进数据库里更新数据
            DeliveryAddress.objects.\
                filter(pk=data_id).update(**user_edit_addrs_form.cleaned_data)
        else:
            res["status"] = 1
            res["errors"] = user_edit_addrs_form.errors

        return JsonResponse(res)
