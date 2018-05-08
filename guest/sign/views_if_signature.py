# -*- coding:utf-8 -*-
'''
带数字签名的验证
'''

from django.contrib import auth as django_auth
import base64
from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist
import hashlib
import time
import requests

# 用户签名+时间戳
def user_sign(request):

    # 通过 POST 方法获取两个参数 time 和 sign 两个参数
    client_time = request.POST.get('time', '')
    client_sign = request.POST.get('sign', '')
    if client_time == '' or client_sign == '':
        return "sign null"

    # 服务器时间
    now_time = time.time()  # unix格式：1466426831
    server_time = str(now_time).split('.')[0]  # Python3 生成的的时间戳精度太高，我们只需要小数点前面的 10 位即可。所以使用 split()函数截取小数点前面的时间

    '''
    获取时间差:
    当服务器端口拿到客户端传来的时间戳后，服务器端也需要重新再获取一下当前时间戳。
    如果服务器端的当前时间戳减法去客户端时间戳小于 60，说明这个接口的请求时间是离现在最近的 60 秒之内。那么 允许接口访问，如果超过 60 秒，则返回“timeout”
    这样就要求请求的客户端不断的获取当前戳作为接口参来访问接口。所以，一直用固定的参数访问接口是无效的
    '''
    time_difference = int(server_time) - int(client_time)
    if time_difference >= 60 :
        return "timeout"

    # 签名检查
    md5 = hashlib.md5()

    '''
    签名参数的生成:
    将api_key(密钥字符串:“&Guest-Bugmaster”)和客户端发来的时间戳,两者拼接成一个新的字符串。并且通过MD5对其进行加密。从而将加密后的字符串作为sign的字段的参数
    '''
    sign_str = client_time + "&Guest-Bugmaster"
    sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)

    # 服务器端以同样的规则来生成这样一个加密后的字符串，从而比较这个串是否相等，如果相等说明签名 验证通过;如果不相等，则返回“sign fail”
    sever_sign = md5.hexdigest()
    if sever_sign != client_sign:
        return "sign error"
    else:
        return "sign right"


# 添加发布会接口--带数字签名
def sec_add_event(request):
    sign_result = user_sign(request)  # 调用签名函数
    if sign_result == "sign null":
        return JsonResponse({'status': 10011, 'message': '用户数字签名为空'})
    elif sign_result == "timeout":
        return JsonResponse({'status': 10012, 'message': '用户数字签名超时'})
    elif sign_result == "sign error":
        return JsonResponse({'status': 10013, 'message': '用户数字签名错误'})
    elif sign_result == "sign right":
        eid = request.POST.get('eid', '')  # 发布会 id
        name = request.POST.get('name', '')  # 发布会标题
        limit = request.POST.get('limit', '')  # 限制人数
        status = request.POST.get('status', '')  # 状态
        address = request.POST.get('address', '')  # 地址
        start_time = request.POST.get('start_time', '')  # 发布会时间

        if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
            return JsonResponse({'status': 10021, 'message': '输入参数为空！'})  # JsonResponse()可以直接将字典转化成 Json 格式返回到客户端

        result = Event.objects.filter(id = eid)
        if result:
            return JsonResponse({'status': 10022, 'message': '发布会id已经存在！'})

        result = Event.objects.filter(name = name)
        if result:
            return JsonResponse({'status': 10023, 'message': '发布会name已经存在！'})

        if status == '':   # 判断发布会状态是否为空，如果为空，将状态设置为 1(True)
            status = 1

        try:
            Event.objects.create(id = eid, name = name, limit = limit, address = address,
                                 status = int(status), start_time = start_time)     # 将数据插入到Event表

        except ValidationError as e:
            error = '日期格式错误！需填写YYYY-MM-DD HH:MM:SS'
            return JsonResponse({'status': 10024, 'message': error})

        return JsonResponse({'status': 200, 'message': '添加发布会成功！'})