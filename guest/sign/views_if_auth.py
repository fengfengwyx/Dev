# -*- coding:utf-8 -*-
'''
带 Auth 认证的接口
'''

from django.contrib import auth as django_auth
import base64
from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist


# 用户认证
def user_auth(request):

    # request.META 是一个 Python 字典，包含了所有本次 HTTP 请求的 Header 信息，比如用户认证、IP 地址和用户 Agent(通常是浏览器的名称和版本号)等
    # HTTP_AUTHORIZATION 用于获取 HTTP authorization,然后，得到的数据是这样的:Basic YWRtaW46YWRtaW4xMjM0NTY=
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')

    # 通过split()方法将上面的结果拆分成list。拆分后的数据是这样的: ['Basic', 'YWRtaW46YWRtaW4xMjM0NTY=']
    auth = get_http_auth.split()


    try:
        # 取出 list 中的加密串，通过 base64 对加密串进行解码。得到的数据是:('admin', ':', 'admin123456')
        auth_parts = base64.b64decode(auth[1]).decode('iso-8859-1').partition(':')
    except IndexError:
        return "null"

    # 最后，取出元组中对应的用户 id 和密码。最终于数据: admin admin123456
    userid, password = auth_parts[0], auth_parts[2]

    # 调用 Django 的认证模块，对得到 Auth 信息进行认证。成功将返回 “success”，失败则返回“fail”
    user = django_auth.authenticate(username=userid, password=password)
    if user is not None and user.is_active:
        django_auth.login(request, user)
        return "success"
    else:
        return "fail"


# 发布会查询---增加用户认证
def sec_get_event_list(request):
    auth_result = user_auth(request)  # 调用认证函数
    if auth_result == "null":
        return JsonResponse({'status': 10011, 'message': '未设置auth'})

    if auth_result == "fail":
        return JsonResponse({'status': 10012, 'message': '用户auth为空或输入错误'})

    eid = request.GET.get("eid", "")
    name = request.GET.get("name", "")

    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': '输入参数为空！'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id = eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': '查询结果为空！'})

        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': '查询成功！', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains = name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': '查询成功！', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': '查询结果为空！'})
