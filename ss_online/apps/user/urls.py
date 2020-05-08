#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 0:48
# @Author  : tanxw
# @Desc    : 子app 路由信息
from django.urls import path
from .views import UserHomeView, UserImageUploadView, UserInfoUpdateView, UserMobileUpdateView, UserPwdUpdateView, \
    UserCourseView, UserFavoriteView, UserMessageView
from django.conf.urls import url

urlpatterns = [
    # 用户个人中心
    path(r'home/', UserHomeView.as_view(), name='home'),
    # 更新用户信息
    path(r'update_info/', UserInfoUpdateView.as_view(), name='update_info'),
    # 修改用户手机号
    path(r'update_mobile/', UserMobileUpdateView.as_view(), name='update_mobile'),
    # 修改用户密码
    path(r'update_pwd/', UserPwdUpdateView.as_view(), name='update_pwd'),
    # 用户头像上传
    path(r'image_upload/', UserImageUploadView.as_view(), name='image_upload'),
    # 用户课程
    path(r'course/', UserCourseView.as_view(), name='course'),
    # 用户收藏
    path(r'<int:fav_type>/favorite/', UserFavoriteView.as_view(), name='favorite'),
    # 用户消息
    path(r'message/', UserMessageView.as_view(), name='message'),
]
