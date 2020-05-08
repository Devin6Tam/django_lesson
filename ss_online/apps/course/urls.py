#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 0:48
# @Author  : tanxw
# @Desc    : 子app 路由信息
from django.urls import path
from .views import CourseListView, CourseDetailView, CourseLessonCommentView, CoursePlayCommentsView
from django.conf.urls import url

urlpatterns = [
    # 课程列表
    path(r'list/', CourseListView.as_view(), name='list'),
    # 课程详情
    path(r'<int:course_id>/detail/', CourseDetailView.as_view(), name='detail'),

    # # 课程-章节列表
    # path(r'<int:course_id>/lesson_list/', CourseLessonsView.as_view(), name='lesson_list'),
    # # 课程-评论列表
    # path(r'<int:course_id>/comment_list/', CourseCommentsView.as_view(), name='comment_list'),
    #
    # # 课程-章节-视频播放
    # path(r'<int:course_id>/<int:lesson_id>/<int:video_id>/video_lesson/', CourseVideoPlayView.as_view(), name='video_lesson'),
    #
    # # 课程-评论-视频播放
    # path(r'<int:course_id>/<int:lesson_id>/<int:video_id>/video_comment/', CourseCommentsPlayView.as_view(), name='video_comment'),

    # 课程章节及评论
    path(r'<int:course_id>/lesson_comment/', CourseLessonCommentView.as_view(), name='lesson_comment'),

    # 课程-评论-视频播放
    path(r'<int:course_id>/<int:lesson_id>/<int:video_id>/play_comment/', CoursePlayCommentsView.as_view(),
         name='play_comment'),
]
