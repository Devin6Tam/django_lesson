from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from apps.course.models import Courses
from apps.organization.models import Teachers, CourseOrg, Teachers
from .models import UserFavorite, CourseComments, Banner
# Create your views here.


from .forms import AddFavForm, AddCommentForm
from ..util import page_util


# 添加收藏
class AddFavView(LoginRequiredMixin, View):
    """
    添加收藏
    :param: LoginRequiredMixin 校验用户是否登录，类似于page_util.not_login
    :param: View 视图对象
    """
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        user = request.user
        # login_flag = page_util.not_login(request)
        # if not login_flag:
        #     return login_flag
        form = AddFavForm(request.POST)
        if form.is_valid():
            fav_type = form.cleaned_data['fav_type']
            fav_id = form.cleaned_data['fav_id']
            user_fav_obj = UserFavorite.objects.filter(user=user, fav_type=fav_type, fav_id=fav_id)
            if user_fav_obj:
                user_fav_obj.delete()
                fav_calc(fav_type, fav_id, is_add=False)
                return JsonResponse({
                    'status': 'success',
                    'msg': '收藏'
                })
            else:
                user_fav_obj = UserFavorite.objects.create(user=user, fav_type=fav_type, fav_id=fav_id)
                user_fav_obj.save()
                fav_calc(fav_type, fav_id)
                return JsonResponse({
                    'status': 'success',
                    'msg': '已收藏'
                })
        else:
            return JsonResponse({'status': 'fail', 'msg': '参数错误'})


# 添加评论
class AddCommentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        user = request.user
        # login_flag = page_util.not_login(request)
        # if not login_flag:
        #     return login_flag
        form = AddCommentForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            comments = form.cleaned_data['comments']
            course_comments_obj = CourseComments(user=user, course=course, comments=comments)
            course_comments_obj.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '参数错误'})


# 首页
class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.order_by('index')
        banner_courses = Courses.objects.filter(is_banner=True).order_by('-add_time')
        index_orgs = CourseOrg.objects.all().order_by('-fav_num')
        return render(request, 'index.html',
                      {'banners': banners,
                       'banner_courses': banner_courses,
                       'index_orgs': index_orgs})




# 收藏统计
# fav_type 收藏类型
# fav_id 收藏ID
# is_add True 记录数+1 False 记录数-1
def fav_calc(fav_type, fav_id, is_add=True):
    if fav_type == 1:
        course = Courses.objects.get(id=fav_id)
        course.fav_num = sub_fav_calc(course.fav_num, is_add)
        course.save()
    if fav_type == 2:
        org = CourseOrg.objects.get(id=fav_id)
        org.fav_num = sub_fav_calc(org.fav_num, is_add)
        org.save()
    if fav_type == 3:
        teacher = Teachers.objects.get(id=fav_id)
        teacher.fav_num = sub_fav_calc(teacher.fav_num, is_add)
        teacher.save()


# 收藏统计
# fav_num 原记录数
# is_add True 记录数+1 False 记录数-1
def sub_fav_calc(fav_num, is_add=True):
    if is_add:
        fav_num += 1
    else:
        fav_num -= 1
    return fav_num
