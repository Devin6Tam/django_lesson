from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import CourseOrg, Citys
from .forms import AddAskForm
from apps.operation.models import UserFavorite


# Create your views here.

# 授课机构列表
from ..util import page_util


class OrgListView(View):
    """查询机构列表"""

    def get(self, request, *args, **kwargs):

        # 获取机构类型，然后进行筛选
        ct = request.GET.get('ct', '')
        citys = Citys.objects.all()[:20]
        city_id = request.GET.get('city', '')
        # 获取排序类型选择
        sort = request.GET.get('sort', '')

        # 第一种方式 使用字典拼接查询提交（支持and）
        # conditions = {}
        # if ct:
        #     conditions['categroy'] = ct
        # if city_id:
        #     conditions['city_id'] = city_id
        # if sort:
        #     orgs = CourseOrg.objects.filter(**conditions).order_by(f'{sort}')
        # else:
        #     orgs = CourseOrg.objects.filter(**conditions)

        # 第二种方式 使用Q查询提交（自由指定and、or）
        con = Q()
        con.connector = 'AND'
        if ct:
            con.children.append(('categroy', ct))
        if city_id:
            con.children.append(('city_id', city_id))

        # F传参方式
        if sort:
            orgs = CourseOrg.objects.filter(con).order_by(f'{sort}')
        else:
            orgs = CourseOrg.objects.filter(con)

        # 第三种方式 条件判断嵌套比较复杂，可以省略
        # if sort == 'students':
        #     if ct:
        #         if city_id:
        #             orgs = CourseOrg.objects.filter(categroy=ct)\
        #                 .filter(city_id=int(city_id)).order_by('-students')
        #         else:
        #             orgs = CourseOrg.objects.filter(categroy=ct).order_by('-students')
        #     else:
        #         if city_id:
        #             orgs = CourseOrg.objects.filter(city_id=int(city_id)).order_by('-students')
        #         else:
        #             orgs = CourseOrg.objects.order_by('-students')
        #
        # elif sort == 'courses':
        #     if ct:
        #         if city_id:
        #             orgs = CourseOrg.objects.filter(categroy=ct) \
        #                 .filter(city_id=int(city_id)).order_by('-course_num')
        #         else:
        #             orgs = CourseOrg.objects.filter(categroy=ct).order_by('-course_num')
        #     else:
        #         if city_id:
        #             orgs = CourseOrg.objects.filter(city_id=int(city_id)).order_by('-course_num')
        #         else:
        #             orgs = CourseOrg.objects.order_by('-students')
        # else:
        #     if ct:
        #         if city_id:
        #             orgs = CourseOrg.objects.filter(city_id=int(city_id)).filter(categroy=ct)
        #         else:
        #             orgs = CourseOrg.objects.filter(categroy=ct)
        #     else:
        #         if city_id:
        #             orgs = CourseOrg.objects.filter(city_id=int(city_id))
        #         else:
        #             orgs = CourseOrg.objects.all()

        num = len(orgs)
        # 机构排名数据较多，取头部3条，采用分片
        orgs_rank = CourseOrg.objects.order_by('-click_num')[:3]

        orgs = page_util.set_page(request, orgs)
        context = {'orgs': orgs,
                   'orgs_rank': orgs_rank,
                   'num': num,
                   'sort': sort,
                   'ct': ct,
                   'citys': citys,
                   'city_id': city_id
                   }

        return render(request, 'org-list.html', context)


# 立即咨询
class AddAskView(View):
    def post(self, request, *args, **kwargs):
        form = AddAskForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["name"])
            print(form.cleaned_data["mobile"])
            print(form.cleaned_data["course_name"])
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '参数错误'})


# 机构详情
class OrgDetailView(View):
    def get(self, request, id, *args, **kwargs):
        # 机构详情查看，点击数加1
        org = CourseOrg.objects.get(id=int(id))
        org.click_num += 1
        org.save()

        # 显示机构课程前3条
        all_courses = org.courses_set.all()[:3]
        # 显示机构讲师前2条
        teachers = org.teachers_set.all()[:2]

        context = set_common_resposne(request, id, org, 2)
        context['all_courses'] = all_courses
        context['teachers'] = teachers
        return render(request, 'org-detail-homepage.html', context)


# 机构课程
class OrgCoursesView(View):
    def get(self, request, id, *args, **kwargs):
        # 机构课程列表
        org = CourseOrg.objects.get(id=int(id))
        courses = org.courses_set.all()
        courses = page_util.set_page(request, courses)

        context = set_common_resposne(request, id, org, 1, 'courses')
        context['courses'] = courses
        return render(request, 'org-detail-course.html', context)


# 机构简介
class OrgDescView(View):
    def get(self, request, id, *args, **kwargs):
        # 机构简介
        org = CourseOrg.objects.get(id=int(id))
        context = set_common_resposne(request, id, org, 2, 'desc')
        return render(request, 'org-detail-desc.html', context)


# 机构讲师
class OrgTeachersView(View):
    def get(self, request, id, *args, **kwargs):
        org = CourseOrg.objects.get(id=int(id))
        teachers = org.teachers_set.all()
        teachers = page_util.set_page(request, teachers)

        context = set_common_resposne(request, id, org, 3, 'teachers')
        context['teachers'] = teachers

        return render(request, 'org-detail-teachers.html', context)


# 获取收藏标志
def is_fav(request, id, fav_type):
    # 未登录显示收藏，已登录根据实际是否收藏来显示
    user = request.user
    if not user.is_authenticated:
        fav_flag = False
    else:
        user_fav_obj = UserFavorite.objects.filter(user=user, fav_id=int(id), fav_type=fav_type)
        if user_fav_obj:
            fav_flag = True
        else:
            fav_flag = False
    return fav_flag


# 设置公共返回信息
# org 机构信息
# fav_flag 收藏标志
# fav_type 收藏类型
# choice 选择
def set_common_resposne(request, id, org, fav_type, choice='home'):
    context = {
        'org': org,
        'fav_flag': is_fav(request, id, fav_type),
        'fav_type': fav_type,
        'choice': choice
    }
    return context
