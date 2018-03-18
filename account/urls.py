"""store_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
import views
urlpatterns = [
    url(r'register/$', views.Register.as_view(), name='register'),
    url(r'check_username/$', views.CheckUsername.as_view(), name='check_username'),
    url(r'activation/$', views.Activation.as_view(), name='activation'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^changepassword', views.ChangePassWord.as_view(), name='changepassword'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^user_center_info/$', views.UserCenterInfo.as_view(), name='user_center_info'),
    url(r'^user_center_site/$', views.UserCenterSite.as_view(), name='user_center_site'),
    url(r'^user_center_set_site/$', views.UserCenterSetSite.as_view(), name='user_center_set_site'),
    url(r'^user_center_del_site/$', views.UserCenterDelSite.as_view(), name='user_conter_del_site'),
    url(r'^user_edit_address/$', views.UserEditAddress.as_view(), name='user_edit_address'),
    url(r'^user_edit_submit/$', views.UserEditSubmit.as_view(), name='user_edit_submit'),
    url(r'^user_center_order/$', views.UserCenterOrder.as_view(), name='user_center_order'),
]
