# -*- coding:utf-8 -*-
'''
采用数字签名验证
'''

import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
import time
import hashlib


class AddSecEventTest(unittest.TestCase):
    ''' 获得发布会列表 '''

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_add_event/"
        # app_key
        self.api_key = "&Guest-Bugmaster"
        # 当前时间
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def tearDown(self):
        print(self.result)  # 打印的结果可以在测试报告中显示（即接口返回数据）

    def test_sec_add_event_sign_null(self):
        ''' 签名参数为空 '''
        payload = {'eid': 1, '': '', 'limit': '', 'address': '', 'start_time': '',
                   'time': '', 'sign': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertEqual(self.result['message'], '用户数字签名为空')

    def test_sec_add_event_time_out(self):
        ''' 请求超时 '''
        now_time = str(int(self.client_time) - 61)
        payload = {'eid': 1, 'name': '', 'limit': '', 'address': '', 'start_time': '',
                   'time': now_time, 'sign': 'abc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertEqual(self.result['message'], '用户数字签名超时')

    def test_sec_add_event_sign_error(self):
        ''' 签名错误 '''
        payload = {'eid': 1, 'name': '', 'limit': '', 'address': '', 'start_time': '',
                   'time': self.client_time, 'sign': 'abc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10013)
        self.assertEqual(self.result['message'], '用户数字签名错误')


    def test_sec_add_event_all_null(self):
        ''' 所有参数为空 '''
        payload = {'eid': '', '': '', 'limit': '', 'address': "",
                   'start_time': '', 'time':self.client_time, 'sign':self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        # 把结果转化为字典赋值给self.result变量，变量加self，是为了在tearDown方法中打印self.result变量
        # 如果不加self，那么只能在每个用力当中都执行打印result变量的语句
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], '输入参数为空！')

    def test_sec_add_event_eid_exist(self):
        ''' id已经存在 '''
        payload = {'eid': 1, 'name': '一加4发布会', 'limit': 2000, 'address': "深圳宝体",
                   'start_time': '2017', 'time':self.client_time, 'sign':self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], '发布会id已经存在！')

    def test_sec_add_event_name_exist(self):
        ''' 名称已经存在 '''
        payload = {'eid': 12, 'name': '红米Pro发布会', 'limit': 2000, 'address': "深圳宝体",
                   'start_time': '2017', 'time':self.client_time, 'sign':self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], '发布会name已经存在！')

    def test_sec_add_event_data_type_error(self):
        ''' 日期格式错误 '''
        payload = {'eid': 12, 'name': '一加5手机发布会', 'limit': 2000, 'address': "深圳宝体",
                   'start_time': '2017', 'time':self.client_time, 'sign':self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('日期格式错误！需填写YYYY-MM-DD HH:MM:SS', self.result['message'])

    def test_sec_add_event_success(self):
        ''' 添加成功 '''
        payload = {'eid': 13, 'name': '一加6手机发布会', 'limit': 2000, 'address': "深圳宝体",
                   'start_time': '2017-05-10 12:00:00', 'time':self.client_time, 'sign':self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], '添加发布会成功！')

if __name__ == '__main__':
    test_data.init_data()  # 初始化接口测试数据
    unittest.main()

