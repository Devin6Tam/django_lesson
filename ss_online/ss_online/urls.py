"""ss_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from .settings import DEBUG
from apps.operation.views import IndexView
from apps.user.views import UserLoginView, UserSmsLoginView, RegisterView, UserLogoutView, SendSmsView
from django.conf.urls import url
import xadmin

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 后台管理平台
    path(r'xadmin/', xadmin.site.urls),
    # 网站首页
    # path(r'', TemplateView.as_view(template_name='index.html'), name="index"),
    path(r'', IndexView.as_view(), name="index"),

    # （密码）登录
    path(r'login/', UserLoginView.as_view(), name='login'),
    # 发送短信
    path(r'send_sms/', SendSmsView.as_view(), name='send_sms'),
    # 短信验证码登录
    path(r'sms_login/', UserSmsLoginView.as_view(), name='sms_login'),
    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    # 退出
    path(r'logout/', UserLogoutView.as_view(), name='logout'),
    # 图形验证码
    path(r'captcha/', include('captcha.urls')),
    # 机构
    path(r'org/', include(('apps.organization.urls', 'organization'), namespace='org')),
    # 课程
    path(r'course/', include(('apps.course.urls', 'course'), namespace='course')),
    # 用户操作
    path(r'op/', include(('apps.operation.urls', 'operation'), namespace='op')),
    # 用户操作
    path(r'user/', include(('apps.user.urls', 'user'), namespace='user')),
    # 媒体文件
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    # # 静态文件 生产必配
    # url(r'^static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),
]

if not DEBUG:  # 生产环境 添加静态目录路由
     urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
     ]