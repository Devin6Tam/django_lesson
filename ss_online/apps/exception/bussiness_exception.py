#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 16:01
# @Author  : tanxw
# @Desc    : 自定义业务异常类

# 业务异常处理类
class BussinessException(Exception):
    def __init__(self, code, error, data):
        self.code = code
        self.error = error
        self.data = data
