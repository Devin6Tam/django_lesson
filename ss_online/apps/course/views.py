from django.shortcuts import render

# Create your views here.
from django.views import View

from .models import Courses

# 课程列表
from ..util import page_util


# 公开课程列表
class CourseListView(View):
    def get(self, request, *args, **kwargs):
        # 获取排序类型选择
        sort = request.GET.get('sort', '')

        # 课程列表
        courses = Courses.objects.all().order_by(f'-{get_order_by(sort)}')
        # 设置分页
        courses = page_util.set_page(request, courses)

        # 热门课程
        hot_courses = Courses.objects.all().order_by(f'-{get_order_by("hot")}')[:1]

        return render(request, 'course-list.html',
                      {'all_courses': courses,
                       'hot_courses': hot_courses,
                       'sort': sort})


# 获取排序字段
def get_order_by(sort):
    if sort == 'hot':
        return 'click_num'
    elif sort == 'students':
        return 'students'
    else:
        return 'add_time'
