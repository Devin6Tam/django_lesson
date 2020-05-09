#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/4 11:01
# @Author  : tanxw
# @Desc    : 中间件使用 - 系统异常定义

from django.shortcuts import render
from apps.exception.bussiness_exception import BussinessException
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class SystemException(MiddlewareMixin):
    def process_exception(request, response, exception):
        if isinstance(exception, BussinessException) and exception.code:
            return render(request, '500.html', {'msg': exception.error})
        else:
            return render(request, '500.html', {'msg': '服务器错误，请稍后重新刷新。'})
