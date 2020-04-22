#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/21 0:27
# @Author  : tanxw
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')