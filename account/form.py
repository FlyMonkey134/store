# -*- coding:utf8 -*-
from django import forms


class RegisterFrom(forms.Form):
    username = forms.CharField(label=u'用户名',required=True,min_length=5,max_length=20)
    password1 = forms.CharField(label=u'密码1',required=True,min_length=8,max_length=20)
    password2 = forms.CharField(label=u'密码2',required=True,min_length=8,max_length=20)
    email = forms.EmailField(label=u'邮箱',required=True)
    allow = forms.CharField(label=u'同意协议',required=True)

    #验证密码是否一致
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password2 != password1 :
            raise forms.ValidationError(u'两次输入的密码不一致',code=password2)
        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名', required=True, min_length=5, max_length=20)
    password = forms.CharField(label=u'密码', required=True, min_length=8, max_length=20)


#修改密码
class ChangePassWord(forms.Form):
    password = forms.CharField(label=u'原密码',required=True,min_length=8,max_length=20)
    password1 = forms.CharField(label=u'密码1', required=True, min_length=8, max_length=20)
    password2 = forms.CharField(label=u'密码2', required=True, min_length=8, max_length=20)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password2 != password1:
            raise forms.ValidationError(u'两次输入的密码不一致，请重新输入',code=password2)
        return password2

#地址(添加，修改)
class UserCenterSiteFrom(forms.Form):
    recipients = forms.CharField(min_length=2,max_length=10,required=True)
    city = forms.CharField(min_length=5,max_length=50,required=True)
    telphone = forms.CharField(min_length=11,max_length=11,required=True)
    address = forms.CharField(min_length=5,max_length=50,required=True)