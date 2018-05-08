# -*- coding:utf-8 -*-
'''
采用AES算法，对客户端的请求进行解密
'''

from Crypto.Cipher import AES
import base64
import json
from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist


#=======AES 加密算法===============
BS = 16
unpad = lambda s : s[0: - ord(s[-1])]

def decryptBase64(src):
    return base64.urlsafe_b64decode(src)

def decryptAES(src, key):
    """
    解析 AES 密文
    """
    src = decryptBase64(src)
    iv = b"1172311105789011"
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    text = cryptor.decrypt(src).decode()
    return unpad(text)

def aes_encryption(request):
    app_key = 'W7v4D60fds2Cmk2U'

    if request.method == 'POST':
        data = request.POST.get("data", "")

    # 解密
    decode = decryptAES(data, app_key)  # 转化为字典
    dict_data = json.loads(decode)
    return dict_data


# 嘉宾查询接口
def sec_get_guest_list(request):
    dict_data = aes_encryption(request)
    eid = dict_data['eid']
    phone = dict_data['phone']

    if eid == '':
        return JsonResponse({'status': 10021, 'message': '关联id不能为空！'})

    if eid != '' and phone == '':
        datas = []
        results = Guest.objects.filter(event_id = eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse({'status': 200, 'message': '查询成功！', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': '查询为空！'})

    if eid != '' and phone != '':
        guest = {}

        try:
            result = Guest.objects.get(phone = phone, event_id = eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': '查询为空！'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status': 200, 'message': '查询成功！', 'data': guest})


'''
1、服务器端与合法客户端约定的密钥 app_key
    app_key = 'W7v4D60fds2Cmk2U'

2、判断客户端请求是否为 POST，通过 POST.get()方法接收 data 参数
    if request.method == 'POST':
        data = request.POST.get("data", "")

3、调用解密函数 decryptAES() ，传参加密字符串和 app_key
    decode = decryptAES(data, app_key)  # 转化为字典

4、调用 decryptBase64()方法，将 Base64 加密字符串解密为 AES 加密字符串
    def decryptBase64(src):
        return base64.urlsafe_b64decode(src)

5、通过 decrypt() 对 AES 加密串进行解密
    def decryptAES(src, key):
        """
        解析 AES 密文
        """
        src = decryptBase64(src)
        iv = b"1172311105789011"
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        text = cryptor.decrypt(src).decode()
        return unpad(text)

6、通过 upad 匿名函数对字符串的长度还原
    BS = 16
    unpad = lambda s : s[0: - ord(s[-1])]

7、将解密后字符串通过 json.loads()方法转化成字典，并将该字典做为 aes_encryption()函数的返回值
    dict_data = json.loads(decode)
    return dict_data

'''