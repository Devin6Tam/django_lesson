from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from apps.course.models import Courses
from apps.organization.models import Teachers, CourseOrg, Teachers
from .models import UserFavorite
# Create your views here.

# 添加收藏功能
from .forms import AddFavForm


class AddFavView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录'
            })
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
