# -*- coding:utf-8 -*-
'''
配置具体接口的二级路径
'''

from django.conf.urls import url
from sign import views_if, views_if_auth, views_if_signature, views_if_AES

app_name='sign'

urlpatterns = [
    # guest system interface:
    # ex : /api/add_event/
    url(r'^add_event/', views_if.add_event, name='add_event'),
    # ex : /api/add_guest/
    url(r'^add_guest/', views_if.add_guest, name='add_guest'),
    # ex : /api/get_event_list/
    url(r'^get_event_list/', views_if.get_event_list, name='get_event_list'),
    # ex : /api/get_guest_list/
    url(r'^get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    # ex : /api/user_sign/
    url(r'^user_sign/', views_if.user_sign, name='user_sign'),
    # 带auth接口
    # ex : /api/sec_get_event_list/
    url(r'^sec_get_event_list/', views_if_auth.sec_get_event_list, name='sec_get_event_list'),
    # 带数字签名接口
    # ex : /api/sec_add_event/
    url(r'^sec_add_event/', views_if_signature.sec_add_event, name='sec_add_event'),
    # 带AES加密解密接口
    # ex : /aip/sec_get_guest_list/
    url(r'^sec_get_guest_list/', views_if_AES.sec_get_guest_list,name='sec_get_guest_list')
]
