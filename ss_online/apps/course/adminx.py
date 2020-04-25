#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 0:23
# @Author  : tanxw

import xadmin
from apps.course.models import Courses, Lessons, Videos, CourseSource


class CourseAdmin(object):
    pass

class LessonAdmin(object):
    pass

class VideoAdmin(object):
    pass

class CourseSourceAdmin(object):
    pass

xadmin.site.register(Courses, CourseAdmin)
xadmin.site.register(Lessons, LessonAdmin)
xadmin.site.register(Videos, VideoAdmin)
xadmin.site.register(CourseSource, CourseSourceAdmin)