#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 0:48
# @Author  : tanxw
# @Desc    : 子app 路由信息
from django.urls import path
from .views import CourseListView
from django.conf.urls import url

urlpatterns = [
    # 机构列表
    path(r'list/', CourseListView.as_view(), name='list'),
]
