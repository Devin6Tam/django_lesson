from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import UserProfile
from .forms import LoginForm, DynamicLoginForm, SmsCodeForm, RegisterForm, UpdateInfoForm, ImageUploadForm, \
    UpdatePwdForm
from django.contrib.auth import authenticate, login, logout
import random
import redis
from django.conf import settings
from apps.util.smsbao.sms_api import sms_send_message, status_str


# Create your views here.
# 用户密码登录
from ..course.models import Courses
from ..operation.models import UserCourse, UserFavorite
from ..organization.models import CourseOrg, Teachers


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
            return render(request, 'login.html',
                          {'form': login_form, 'is_sms_login': is_sms_login, 'captcha_form': captcha_form})


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


# 用户个人中心
class UserHomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        form = DynamicLoginForm()
        return render(request, 'user/usercenter-info.html', {"form": form})


# 用户信息修改
class UserInfoUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):

        # 传入instance=request.user,这样保存的时候，不会新增数据
        form = UpdateInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(form.errors)


# 用户手机号修改
class UserMobileUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        user = request.user
        login_form = SmsCodeForm(request.POST)
        if login_form.is_valid():
            user.mobile = login_form.cleaned_data['mobile']
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(login_form.errors)


# 用户密码修改
class UserPwdUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):

        form = UpdatePwdForm(request.POST)
        if form.is_valid():
            old_pwd = form.cleaned_data['password1']
            new_pwd = form.cleaned_data['password2']
            user = authenticate(username=request.user.username, password=old_pwd)
            if user:
                user.set_password(new_pwd)
                user.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '原密码错误'})
        else:
            return JsonResponse(form.errors)


# 用户头像上传
class UserImageUploadView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(form.errors)


class UserCourseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):

        user_courses = UserCourse.objects.filter(user=request.user)

        all_courses = [user_course.course for user_course in user_courses]
        return render(request, 'user/usercenter-mycourse.html', {'all_courses': all_courses})


class UserFavoriteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, fav_type, *args, **kwargs):
        user_favorites = UserFavorite.objects.filter(user=request.user, fav_type=fav_type)
        fav_ids = [user_favorite.fav_id for user_favorite in user_favorites]
        if fav_type == 1:
            all_courses = Courses.objects.filter(id__in=fav_ids)
            return render(request, 'user/usercenter-fav-course.html', {'all_courses': all_courses, 'fav_type': fav_type})
        elif fav_type == 2:
            all_orgs = CourseOrg.objects.filter(id__in=fav_ids)
            return render(request, 'user/usercenter-fav-org.html', {'all_orgs': all_orgs, 'fav_type': fav_type})
        elif fav_type == 3:
            all_tearchers = Teachers.objects.filter(id__in=fav_ids)
            return render(request, 'user/usercenter-fav-teacher.html', {'all_tearchers': all_tearchers, 'fav_type': fav_type})


class UserMessageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        return render(request, 'user/usercenter-message.html')