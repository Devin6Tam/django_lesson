from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import UserProfile
from .forms import LoginForm, DynamicLoginForm, SmsCodeForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
import random
import redis
from django.conf import settings
from apps.util.smsbao.sms_api import sms_send_message, status_str


# Create your views here.
# 用户密码登录
class UserLoginView(View):
    """get请求的时候，展示页面"""
    def get(self, request, *args, **kwargs):
        # return render(request, 'login.html')
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        form = DynamicLoginForm()
        return render(request, 'login.html', {'form': form})

    """处理用户密码登录请求"""
    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # username = request.POST.get('username')
            # password = request.POST.get('password')
            print((username, password))
            #  验证用户是否存在
            user = authenticate(username=username, password=password)
            # user = UserProfile.objects.filter(username=username, password=password)
            if user:
                #  登录的操作，实际上是配置cookie和sessionid
                login(request, user=user)
                # return HttpResponse('OK!')
                #  不会产生url的变化
                # return render(request, 'index.html')
                return redirect(reverse('index'), {'request': request})
            else:
                # return HttpResponse('invalid password')

                return render(request, 'login.html', {'form': login_form, 'msg': '用户名或者密码错误'})
        else:
            return render(request, 'login.html', {'form': login_form})


# 用户短信验证码登录
class UserSmsLoginView(View):

    """处理短信验证码登录"""
    def post(self, request, *args, **kwargs):
        is_sms_login = True
        login_form = SmsCodeForm(request.POST)
        if login_form.is_valid():
            mobile = login_form.cleaned_data['mobile']
            user = UserProfile.objects.filter(username=mobile)
            if user:
                user = user[0]
            else:
                user = UserProfile()
                user.username = mobile
                user.mobile = mobile
                user.set_password('%06d' % random.randint(0, 999999))
                user.save()
            login(request, user)
            return redirect('index')
        else:
            captcha_form = DynamicLoginForm()
            return render(request, 'login.html', {'form': login_form, 'is_sms_login': is_sms_login, 'captcha_form': captcha_form})

# 发送短信
class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        form = DynamicLoginForm(request.POST)
        ret_dict = {}
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            verify_code = '%06d' % random.randint(0, 999999)
            print(verify_code)
            # status_code = sms_send_message(mobile, verify_code)
            status_code = '0'
            if status_code == '0':
                # redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                #                          db=settings.REDIS_DB, password=settings.REDIS_PASSWORD, encoding='utf8')
                redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                         db=settings.REDIS_DB, encoding='utf8')
                redis_conn.setex(mobile, 5 * 60, verify_code)

                ret_dict['status'] = 'success'
                return JsonResponse(ret_dict)
            else:
                ret_dict['msg'] = status_str[status_code]
                return JsonResponse(ret_dict)
        # ret_dict['msg'] = '参数错误'
        for k, v in form.errors.items():
            ret_dict[k] = v[0]
        return JsonResponse(ret_dict)

class RegisterView(View):
    """访问注册页面，并加载图形码"""
    def get(self, request, *args, **kwargs):
        captcha_form = DynamicLoginForm()
        return render(request, 'register.html', {'captcha_form': captcha_form})

    """处理注册请求"""
    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            mobile = register_form.cleaned_data['mobile']
            password = register_form.cleaned_data['password']
            user = UserProfile()
            user.username = mobile
            user.mobile = mobile
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('index')
        captcha_form1 = DynamicLoginForm()
        return render(request, 'register.html', {'form': register_form, 'captcha_form1': captcha_form1})

# 用户登出
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login'))
