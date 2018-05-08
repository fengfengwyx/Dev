"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from sign import views  #导入 sign 应用 views 文件

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^index/$',views.index),  #添加index/路径配置
    url(r'^login_action/$', views.login_action),  #添加login_action/路径处理登录请求
    url(r'^event_manage/$', views.event_manage),
    url(r'^$', views.index),
    url(r'^accounts/login/$', views.index),
    url(r'^search_name/$', views.search_name),
    url(r'^guest_manage/$', views.guest_manage),
    url(r'^search_realname/$', views.search_realname),
    # (?P<event_id>[0-9]+) 配置二级目录，发布会 id，要求必须为数字
    url(r'^sign_index/(?P<event_id>[0-9]+)/$', views.sign_index),
    # 签到动作的路由
    url(r'^sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action),
    url(r'^logout/$', views.logout),
    url(r'^api/', include('sign.urls', namespace='sign')),
]


'''
url(r'^index/$',views.index)
python正则表达式

r: 字符串前面加“ r ”是为了防止字符串中出现类似“\t”字符时被转义
^: 匹配字符串开头;在多行模式中匹配每一行的开头。 ^abc abc
$: 匹配字符串末尾;在多行模式中匹配每一行末尾。 abc$ abc

'''