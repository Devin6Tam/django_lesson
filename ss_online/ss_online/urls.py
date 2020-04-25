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
from django.contrib import admin
from django.urls import path

import xadmin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # # 用户模块
    # path('user/', admin.site.urls),
    # # 课程模块
    # path('cource/', admin.site.urls),
    # # 培训机构模块
    # path('organization/', admin.site.urls),
    # # 用户操作模块
    # path('operation/', admin.site.urls),
    # # 讲师模块
    # path('teacher/', admin.site.urls),
]
