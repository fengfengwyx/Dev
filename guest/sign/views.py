'''

视图在Django 中是连接页面与数据的中间纽带。

拿登录的例子来讲，用户在页面上输入了用户名和密码点击登录。那么request请求会由视图来接收，如何提取出用户名和密码的数据，
如何用这些数据去查询数据库，再如何将登录成功的页面返回给用户，这些全部由视图层来完成

'''

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 登录页面
def index(request):
    # 该函数的第一个参数是请求对象的，第二个参数返回一个index.html 页面
    return render(request, "index.html")

# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username, password = password)  # 使用 authenticate()函数认证给出的用户名和密码
        if user is not None:
            auth.login(request, user)  # 登录
            request.session['user'] = username  # 将 session 信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')  # HttpResponseRedirect  对路径进行重定向，从而将登录成功之后的请求 指向/event_manage/目录
            return response
        else:
            return render(request, 'index.html', {'error':'username or password error!'})

# 发布会管理
@login_required
def event_manage(request):
    username = request.session.get('user', '')
    event_list = Event.objects.all()

    paginator = Paginator(event_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "event_manage.html", {"user": username,
                                                 "events": contacts})

# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)

    paginator = Paginator(event_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "event_manage.html", {"user": username,
                                                 "events": contacts})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()

    # 分页
    # 把查询出来的所有嘉宾列表guest_list放到Paginator类中，划分每页显示2条数据
    paginator = Paginator(guest_list, 2)

    # 通过 GET 请求得到当前要显示第几页的数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        # 获取第 page 页的数据。如果当前没有页数，抛 PageNotAnInteger 异常，返回第一页的数据
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        # 如果超出最 大页数的范围，抛 EmptyPage 异常，返回最后一页面的数据
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})

# 嘉宾名称搜索
@login_required
def search_realname(request):
    username = request.session.get('user', '')
    search_realname = request.GET.get("realname", "")
    guest_list = Guest.objects.filter(realname__contains=search_realname)

    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})


# 签到页面
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})

# 签到动作
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone','')

    # 查询 Guest 表判断用户输入的手机号是否存在，如果不存在将显示用户“手机号为空或不存在”
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error.'})

    # 通过手机和发布会id两个条件来查询 Guest 表，如果结果为空表示用户“该用户未参加此次发布会”
    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.'})

    # 再通过手机号查询 Guest 表，判断该手机号的签到状态是否为 1，如果为 1，表示已经签过到了， 返回用户“已签到”
    result = Guest.objects.get(phone=phone,event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': "user has sign in."})

    # 否则，显示用户“签到成功!”，并返回签到用户的信息
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint':'sign in success!',
                                                   'guest': result})

# 退出登录
@login_required
def logout(request):
    # auth.logout()函数用于系统的退出，它可以清除掉浏览器保存的用户信息，所以不用再考虑如何删除浏览器cookie等问题
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response

