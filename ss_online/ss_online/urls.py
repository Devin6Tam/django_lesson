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
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.static import serve

from apps.user.views import UserLoginView, UserSmsLoginView, RegisterView, UserLogoutView, SendSmsView
from django.conf.urls import url
import xadmin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'xadmin/', xadmin.site.urls),
    path(r'', TemplateView.as_view(template_name='index.html'), name="index"),
    path(r'login/', UserLoginView.as_view(), name='login'),
    path(r'send_sms/', SendSmsView.as_view(), name='send_sms'),
    path(r'sms_login/', UserSmsLoginView.as_view(), name='sms_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path(r'logout/', UserLogoutView.as_view(), name='logout'),
    path(r'captcha/', include('captcha.urls')),
    path(r'org/', include(('apps.organization.urls', 'organization'), namespace='org')),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]
