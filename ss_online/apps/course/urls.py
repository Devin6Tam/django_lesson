#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 0:48
# @Author  : tanxw
# @Desc    : 子app 路由信息
from django.urls import path
from .views import CourseListView, CourseDetailView, CourseLessonsView, CourseCommentsView, CourseAddCommentView
from django.conf.urls import url

urlpatterns = [
    # 课程列表
    path(r'list/', CourseListView.as_view(), name='list'),
    # 课程详情
    path(r'<int:course_id>/detail/', CourseDetailView.as_view(), name='detail'),

    # 课程-章节详情
    path(r'<int:course_id>/lesson_list/', CourseLessonsView.as_view(), name='lesson_list'),
    # 课程-评论
    path(r'<int:course_id>/comment_list/', CourseCommentsView.as_view(), name='comment_list'),
    # 课程-添加评论
    path(r'<int:course_id>/add_comment/', CourseAddCommentView.as_view(), name='add_comment'),
]
