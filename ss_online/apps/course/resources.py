#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 23:43
# @Author  : tanxw

from import_export import resources
from .models import Courses
class CourseResource(resources.ModelResource):
    class Meta:
        model = Courses
        fields = ['id', 'name', 'teacher', 'desc']
