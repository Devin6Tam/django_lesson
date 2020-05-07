import random

from django.shortcuts import render

# Create your views here.
from django.views import View

from .models import Courses, CourseTags

from ..operation.models import UserCourse
from ..util import page_util


# 公开课程列表
class CourseListView(View):
    def get(self, request, *args, **kwargs):
        # 获取排序类型选择
        sort = request.GET.get('sort', '')

        # 课程列表
        courses = Courses.objects.order_by(f'-{page_util.get_order_by(sort)}')
        # 设置分页
        courses = page_util.set_page(request, courses)

        # 热门课程
        hot_courses = Courses.objects.order_by(f'-{page_util.get_order_by("hot")}')[:1]

        return render(request, 'course-list.html',
                      {'all_courses': courses,
                       'hot_courses': hot_courses,
                       'sort': sort})


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        # 获取课程详情
        course = Courses.objects.get(id=int(course_id))

        # 获取学习该课程的用户信息
        user_courses = UserCourse.objects.filter(course=course)
        # 可以使用列表推导式
        # students = [user_course.user for user_course in user_courses]
        students = []
        for user_course in user_courses:
            if len(students) <= 3:
                students.append(user_course.user)
            else:
                break

        # 查询当前课程的所有tag
        tag_objs = CourseTags.objects.filter(course=course)
        tags = [tag_obj.tag for tag_obj in tag_objs]
        # 通过tags查询满足条件的课程,过滤掉本身
        related_course_ids = CourseTags.objects.filter(tag__in=tags).exclude(course=course)
        #  使用set去重
        related_courses = list(set([related_course_id.course for related_course_id in related_course_ids]))
        #  在相关的课程列表中随机的取出一个课程
        if len(related_courses) > 1:
            related_course = random.choice(related_courses)
        else:
            related_course = None
        # 课程、机构收藏标识获取
        course_fav_flag = page_util.is_fav(request, course.id, 1)
        org_fav_flag = page_util.is_fav(request, course.course_org.id, 2)

        return render(request, 'course-detail.html',
                      {'course': course,
                       'students': students,
                       'related_course': related_course,
                       'course_fav_flag': course_fav_flag,
                       'org_fav_flag': org_fav_flag})