from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import UserProfile
from .forms import LoginForm, DynamicLoginForm, SmsCodeForm
from django.contrib.auth import authenticate, login, logout
import random
import redis
from django.conf import settings


# Create your views here.
# 用户登录
class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'login.html')
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        form = DynamicLoginForm()
        return render(request, 'login.html', {'form': form})

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


# 用户登出
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login'))


# 发送短信
class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        form = DynamicLoginForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            verify_code = '%08d' % random.randint(0, 999999)
            print(verify_code)
            # redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
            #                          db=settings.REDIS_DB, password=settings.REDIS_PASSWORD, encoding='utf8')
            redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     db=settings.REDIS_DB, encoding='utf8')
            redis_conn.setex(mobile, 5 * 60, verify_code)
            return JsonResponse('OK!')
        return HttpResponse('error!')
