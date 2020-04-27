#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 0:23
# @Author  : tanxw

import xadmin
from .models import Courses, Lessons, Videos, CourseSource


class CourseAdmin(object):
    # 列表页显示字段
    list_display = ['name', 'desc', 'tearcher', 'course_org', 'degree', 'learn_time', 'category']
    # 支持搜索的字段
    search_fields = ['name']
    # 过滤筛选的字段
    list_filter = ['name']
    # 列表字段支持编辑
    list_editable = ['name', 'degree', 'category']
    # 分页
    list_per_page = 10

class LessonAdmin(object):
    # 列表页显示字段
    list_display = ['course', 'name', 'learn_time']
    # 支持搜索的字段
    search_fields = ['name']
    # 过滤筛选的字段
    list_filter = ['name']
    # 列表字段支持编辑
    list_editable = ['name']
    # 分页
    list_per_page = 10

class VideoAdmin(object):
    # 列表页显示字段
    list_display = ['lesson', 'name', 'learn_time']
    # 支持搜索的字段
    search_fields = ['name']
    # 过滤筛选的字段
    list_filter = ['name']
    # 列表字段支持编辑
    list_editable = ['name']
    # 分页
    list_per_page = 10

class CourseSourceAdmin(object):
    # 列表页显示字段
    list_display = ['course', 'name', 'file']
    # 支持搜索的字段
    search_fields = ['name']
    # 过滤筛选的字段
    list_filter = ['name']
    # 列表字段支持编辑
    list_editable = ['name']
    # 分页
    list_per_page = 10

xadmin.site.register(Courses, CourseAdmin)
xadmin.site.register(Lessons, LessonAdmin)
xadmin.site.register(Videos, VideoAdmin)
xadmin.site.register(CourseSource, CourseSourceAdmin)