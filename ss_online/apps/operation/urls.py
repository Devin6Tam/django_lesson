#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 0:48
# @Author  : tanxw
# @Desc    : 子app 路由信息
from django.urls import path, include
from .views import AddFavView, AddCommentView

urlpatterns = [
    path(r'add_fav/', AddFavView.as_view(), name='add_fav'),
    # 课程-添加评论
    path(r'add_comment/', AddCommentView.as_view(), name='add_comment'),
]
