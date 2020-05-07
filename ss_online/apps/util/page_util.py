#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 18:12
# @Author  : tanxw
# @Desc    : 分页帮助工具

from pure_pagination import Paginator, PageNotAnInteger

from apps.operation.models import UserFavorite


# 封装分页数据
def set_page(request, objs, per_page=10):
    """
    封装分页数据
    :param request: 请求对象
    :param objs: 数据集合
    :param per_page: 页面显示条数
    :return: objs
    """
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(objs, request=request, per_page=per_page)
    objs = p.page(page)
    return objs


# 获取收藏标志
def is_fav(request, fav_id, fav_type):
    """
    获取收藏标志
    :param request: 请求对象
    :param fav_id: 收藏id
    :param fav_type: 收藏类型
    :return: fav_flag 收藏标识
    """
    # 未登录显示收藏，已登录根据实际是否收藏来显示
    user = request.user
    if not user.is_authenticated:
        fav_flag = False
    else:
        user_fav_obj = UserFavorite.objects.filter(user=user, fav_id=int(fav_id), fav_type=fav_type)
        if user_fav_obj:
            fav_flag = True
        else:
            fav_flag = False
    return fav_flag


# 获取排序字段
def get_order_by(sort):
    if sort == 'hot':
        return 'click_num'
    elif sort == 'students':
        return 'students'
    else:
        return 'add_time'


# 获取排序字段
def get_org_order_by(sort):
    if sort == 'courses':
        return 'course_num'
    elif sort == 'students':
        return 'students'
    else:
        return 'add_time'