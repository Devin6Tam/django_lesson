#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 18:12
# @Author  : tanxw
# @Desc    : 分页帮助工具

from pure_pagination import Paginator, PageNotAnInteger


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
