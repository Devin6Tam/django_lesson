#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 0:48
# @Author  : tanxw
# @Desc    : 子app 路由信息
from django.urls import path, include
from django.views.generic import TemplateView
from .views import AddFavView

urlpatterns = [
    path(r'add_fav/', AddFavView.as_view(), name='add_fav'),
]
