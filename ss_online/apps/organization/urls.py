#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 0:48
# @Author  : tanxw
# @Desc    : 子app 路由信息
from django.urls import path, include
from django.views.generic import TemplateView
from .views import OrgListView, AddAskView, OrgDetailView

urlpatterns = [
    path(r'list/', OrgListView.as_view(), name='list'),
    path(r'add_ask/', AddAskView.as_view(), name='add_ask'),
    path(r'<int:id>/', OrgDetailView.as_view(), name='org_detail'),
]
