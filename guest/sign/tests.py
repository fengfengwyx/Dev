'''
发布会管理、嘉宾管理的测试想要运行通过，需要在 views.py 视图文件中将
event_manage()、search_name()、guest_manage()、search_phone()、sign_index_action()函数的 @login_required 装饰器去掉，
因为这两个函数依赖于登录，而Client()所提供的 get()和 post()方法并没有验证登录的参数
'''


from django.test import TestCase,Client
from sign.models import Event,Guest
from django.contrib.auth.models import User
from datetime import datetime

# Create your tests here.

# Test Models
class ModelTest(TestCase):

    # 在 setUp()初始化方法中，创建一条发布会和嘉宾数据。Django 在执行 setUp()方法中的数据库初始化时，并非真正的向数据库表中插入了数据。所以，数据库并不会因为运行测试而产生测试数据
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000,
                             address='shenzhen', start_time='2016-08-31 02:18:22')

        Guest.objects.create(id=1, event_id=1, realname='alen',
                             phone='13711001101',email='alen@mail.com', sign=False)


    def test_event_models(self):
        result = Event.objects.get(name = "oneplus 3 event")
        self.assertEqual(result.address, "beijing")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone = "13711001101")
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)

# Test Index
class IndexPageTest(TestCase):
    # 测试 index 登录首页

    def test_index_page_renders_index_template(self):
        # 测试 index 视图
        response = self.client.get('/')
        # assertEqual()服务器对客户端的应答是否 为 200
        self.assertEqual(response.status_code, 200)
        # assertTemplateUsed()断言是否用给定的是index.html 模版响应
        self.assertTemplateUsed(response, 'index.html')

# Test Login action
class LoginActionTest(TestCase):
    # 测试登录函数

    # 在setUp()初始化方法中，调用 User.objects.create_user()创建登录用户数据
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        self.c = Client()

    # 用户名密码若为空
    def test_login_action_username_password_null(self):
        test_data = {'username': '', 'password': ''}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    # 用户名密码错误
    def test_login_action_username_password_error(self):
        test_data = {'username': 'abc', 'password': '123'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    # 登录成功
    def test_login_action_success(self):
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.c.post('/login_action/', data=test_data)
        # 在 login_action 视图函数中，当用户登录验证成功后，通过 HttpResponseRedirect('/event_manage/') 跳转到了发布会管理视图，这是一个重定向，所以HTTP返回码是302
        self.assertEqual(response.status_code, 302)


# Test Event Manage
class EventManageTest(TestCase):
    # 发布会管理

    def setUp(self):
        Event.objects.create(id=2, name='xiaomi5', limit=2000, status=True,
                             address='beijing', start_time=datetime(2016, 8, 10, 14, 0, 0))
        self.c = Client()

    # 测试发布会是否存在:xiaomi5
    def test_event_manage_success(self):
        response = self.c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    # 测试发布会搜索内容是否存在
    def test_event_manage_search_success(self):
        response = self.c.post('/search_name/', {"name": "xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

# Test Guest Manage
class GuestManageTest(TestCase):
    # 嘉宾管理
    def setUp(self):
        Event.objects.create(id=1, name="xiaomi5", limit=2000,
                             address='beijing', status=1, start_time=datetime(2016, 8, 10, 14, 0, 0))

        Guest.objects.create(realname="alen", phone=18611001100,
                             email='alen@mail.com', sign=0, event_id=1)
        self.c = Client()

    # 测试嘉宾信息是否存在: alen
    def test_event_manage_success(self):
        response = self.c.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)

    # 测试嘉宾搜索内容是否存在
    def test_guest_manage_search_success(self):
        response = self.c.post('/search_realname/', {"realname": "alen"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)

# Test User Sign
class SignIndexActionTest(TestCase):
    # 发布会签到

    def setUp(self):
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address='beijing',
                             status=1, start_time='2017-8-10 12:30:00')
        Event.objects.create(id=2, name="oneplus4", limit=2000, address='shenzhen',
                             status=1, start_time='2017-6-10 12:30:00')
        Guest.objects.create(realname="alen", phone=18611001100,
                             email='alen@mail.com', sign=0, event_id=1)
        Guest.objects.create(realname="una", phone=18611001101,
                             email='una@mail.com', sign=1, event_id=2)
        self.c = Client()

    # 手机号为空
    def test_sign_index_action_phone_null(self):
        response = self.c.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    # 手机号或发布会 id 错误
    def test_sign_index_action_phone_or_event_id_error(self):
        response = self.c.post('/sign_index_action/2/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    # 用户已签到
    def test_sign_index_action_user_sign_has(self):
        response = self.c.post('/sign_index_action/2/', {"phone": "18611001101"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    # 签到成功
    def test_sign_index_action_sign_success(self):
        response = self.c.post('/sign_index_action/1/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)