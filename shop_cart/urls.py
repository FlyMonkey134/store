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
from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^add_cart/(?P<gid>\d+)/$',views.AddCart.as_view(),name='add_cart'),
    url(r'^shop_cart/$', views.ShowShopCart.as_view(),name='shop_cart'),
    url(r'^del_shop_cart/(?P<gid>\d+)/$', views.DelShopCart.as_view(), name='del_shop_cart'),
    url(r'^update_cart/(?P<gid>\d+)$', views.UpdateCart.as_view(), name='update_cart')
]
