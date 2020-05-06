#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 0:48
# @Author  : tanxw
# @Desc    : 子app 路由信息
from django.urls import path
from .views import OrgListView, AddAskView, OrgDetailView, OrgCoursesView, OrgDescView, OrgTeachersView, TeachersListView, TeachersDetailView
from django.conf.urls import url

urlpatterns = [
    # 机构列表
    path(r'list/', OrgListView.as_view(), name='list'),
    # 立即咨询
    path(r'add_ask/', AddAskView.as_view(), name='add_ask'),
    # 机构（首页）详情
    path(r'<int:id>/', OrgDetailView.as_view(), name='detail'),
    # path(r'<int:id>/courses', OrgCoursesView.as_view(), name='courses'),
    # 机构课程
    url(r'(?P<id>\d+)/courses$', OrgCoursesView.as_view(), name='courses'),
    # 机构简介
    path(r'<int:id>/desc/', OrgDescView.as_view(), name='desc'),
    # 机构老师
    path(r'<int:id>/teachers/', OrgTeachersView.as_view(), name='teachers'),
    # 讲师列表
    path(r'teachers/list', TeachersListView.as_view(), name='teachers_list'),
    # 讲师详情
    path(r'teachers/<int:id>/detail', TeachersDetailView.as_view(), name='teachers_detail'),
]
