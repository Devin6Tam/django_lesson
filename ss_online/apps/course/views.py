import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from .models import Courses, CourseTags, Videos, Lessons

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

        return render(request, 'course/course-list.html',
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

        return render(request, 'course/course-detail.html',
                      {'course': course,
                       'students': students,
                       'related_course': related_course,
                       'course_fav_flag': course_fav_flag,
                       'org_fav_flag': org_fav_flag})


"""
已优化处理，采用更简便的前端交互方式

# 查看课程章节信息
class CourseLessonsView(LoginRequiredMixin, View):
    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=int(course_id))
        context = lesson_common(course, 'video')
        return render(request, 'course-video.html', context)


# 查看课程评论
class CourseCommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=int(course_id))
        # 所有评论
        all_comments = course.coursecomments_set.order_by('-add_time')
        all_comments = page_util.set_page(request, all_comments)

        context = lesson_common(course, 'comment')
        context['all_comments'] = all_comments

        return render(request, 'course-comment.html', context)


class CourseVideoPlayView(LoginRequiredMixin, View):
    def get(self, request, course_id, lesson_id, video_id, *args, **kwargs):
        course = Courses.objects.get(id=int(course_id))
        lesson = Lessons.objects.get(id=lesson_id, course_id=course_id)
        video = Videos.objects.get(id=int(video_id), lesson=lesson)

        context = lesson_common(course, 'play_video')
        context['lesson'] = lesson
        context['video'] = video

        return render(request, 'course-play-video.html', context)


class CourseCommentsPlayView(LoginRequiredMixin, View):
    def get(self, request, course_id, lesson_id, video_id, *args, **kwargs):

        course = Courses.objects.get(id=int(course_id))
        lesson = Lessons.objects.get(id=lesson_id, course_id=course_id)
        video = Videos.objects.get(id=int(video_id), lesson=lesson)
        # 所有评论
        all_comments = course.coursecomments_set.order_by('-add_time')
        all_comments = page_util.set_page(request, all_comments)

        context = lesson_common(course, 'play_comment')
        context['lesson'] = lesson
        context['video'] = video
        context['all_comments'] = all_comments
        return render(request, 'course-play-comment.html', context)
"""

class CourseLessonCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, course_id, *args, **kwargs):

        course = Courses.objects.get(id=int(course_id))
        # 所有评论
        all_comments = course.coursecomments_set.order_by('-add_time')
        all_comments = page_util.set_page(request, all_comments)

        context = lesson_common(course, 'lesson')
        context['all_comments'] = all_comments
        return render(request, 'course/course-lesson.html', context)


class CoursePlayCommentsView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, course_id, lesson_id, video_id, *args, **kwargs):

        course = Courses.objects.get(id=int(course_id))
        lesson = Lessons.objects.get(id=lesson_id, course_id=course_id)
        video = Videos.objects.get(id=int(video_id), lesson=lesson)
        # 所有评论
        all_comments = course.coursecomments_set.order_by('-add_time')
        all_comments = page_util.set_page(request, all_comments)

        context = lesson_common(course, 'video')
        context['lesson'] = lesson
        context['video'] = video
        context['all_comments'] = all_comments
        return render(request, 'course/course-play.html', context)


# 课程章节公共模块
def lesson_common(course, choice):
    """
    课程章节公共模块
    :param: course 课程信息
    :param: choice 选择，用于tab切换高亮显示
    :param: context 返回字典
    """
    # 获取该用户其他课程信息
    user_courses = UserCourse.objects.filter(course_id=course.id).exclude(course=course)
    if len(user_courses) > 5:
        user_courses = user_courses[:5]
    related_courses = list(set([user_course.course for user_course in user_courses]))

    context = {
        'course': course,
        'related_courses': related_courses,
        'choice': choice
    }
    return context
