# -*- coding:utf-8 -*-
'''
采用AES加密算法
'''

import base64
import requests
import unittest
import json
from db_fixture import test_data
from Crypto.Cipher import AES

'''
加密的过程是在客户端进行的，也就是在本测试用例中
'''

class AEStest(unittest.TestCase):

    def setUp(self):
        BS = 16
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        self.base_url = "http://127.0.0.1:8000/api/sec_get_guest_list/"
        self.app_key = 'W7v4D60fds2Cmk2U'

    def tearDown(self):
        print(self.result)

    def encryptBase64(self, src):
        return base64.urlsafe_b64encode(src)

    def encryptAES(self, src, key):
        """
        生成 AES 密文
        """
        iv = b"1172311105789011"  # 必须是 16 位字节
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cryptor.encrypt(self.pad(src))
        return self.encryptBase64(ciphertext)

    def test_aes_interface(self):
        '''test aes interface'''
        payload = {'eid': '1', 'phone': '13511001100'}
        # 加密
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], "查询成功！")

    def test_sec_get_guest_list_eid_null(self):
        ''' eid 参数为空 '''
        payload = {'eid': '', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={'data':encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], '关联id不能为空！')

    def test_sec_get_event_list_eid_error(self):
        ''' 根据 eid 查询结果为空 '''
        payload = {'eid': '901', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={'data':encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], '查询为空！')

    def test_sec_get_event_list_eid_success(self):
        ''' 根据 eid 查询结果成功 '''
        payload = {'eid': '1', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={'data':encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], '查询成功！')
        self.assertEqual(self.result['data'][0]['realname'],'alen')
        self.assertEqual(self.result['data'][0]['phone'],'13511001100')

    def test_sec_get_event_list_eid_phone_null(self):
        ''' 根据 eid 和phone 查询结果为空 '''
        payload = {'eid': '2', 'phone': '10000000000'}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={'data':encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], '查询为空！')

    def test_sec_get_event_list_eid_phone_success(self):
        ''' 根据 eid 和phone 查询结果成功 '''
        payload = {'eid': '1', 'phone': '13511001100'}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={'data':encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], '查询成功！')
        self.assertEqual(self.result['data']['realname'],'alen')
        self.assertEqual(self.result['data']['phone'],'13511001100')


if __name__ == '__main__':
    test_data.init_data() # 初始化接口测试数据
    unittest.main()

'''
1、定义 app_key 和接口参数，app_key 是密钥，只有合法调用者才知道
    self.app_key = 'W7v4D60fds2Cmk2U'
    payload = {'eid': '1', 'phone': '13800138000'}

2、将 payload 参数转化为 json 格式，然后将参数和 app_key 传参给 encryptAES()方法用于生成加密串
    encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

3、通过 encrypt()方法对 src 接口参数生成 加密串

    def encryptAES(self, src, key):
        """
        生成 AES 密文
        """
        iv = b"1172311105789011"  # 必须是 16 位字节
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cryptor.encrypt(self.pad(src))
        return self.encryptBase64(ciphertext)

注意：encrypt()要加密的字符串有严格的长度要求，长度必须是 16 的倍数。如果直接生成会报错

4、因此，对参数字符串处理，使其长度固定
    self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

注意：生成的字符串如下，字符串过长，不适合传输
    b'>_\x80\x1fi\x97\x8f\x94~\xeaE\xectBm\x9d\xa9\xc5\x85<+e\xa5lW\xe1\x84}\xfa\x8b\xb9\xde\x1a\x10J\xcd\ xc5\xa1A4Z\xff\x05x\xe3\xf1\x00Z'

5、通过 base64 模块的 urlsafe_b64encode()方法对 AES 加密串进行二次加密
    def encryptBase64(self, src):
        return base64.urlsafe_b64encode(src)

得到的字符串是这样的: b'gouBbuKWEeY5wWjMx-nNAYDTion0ADOysaLw1uzzGOpvTTASpQGJu5p0WuDhZMiM'

6、将加密后的字符串作为接口的 data 参数发送给接口
    r = requests.post(self.base_url, data={"data": encoded})
'''

