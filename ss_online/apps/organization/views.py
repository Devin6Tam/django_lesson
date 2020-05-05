from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from apps.organization.models import CourseOrg
from django.views import View
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import CourseOrg, Citys
from .forms import AddAskForm
from apps.operation.models import UserFavorite


# Create your views here.

class OrgListView(View):
    """查询机构列表"""

    def get(self, request, *args, **kwargs):

        # 获取机构类型，然后进行筛选
        ct = request.GET.get('ct', '')
        citys = Citys.objects.all()
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
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(orgs, request=request, per_page=5)
        orgs = p.page(page)
        context = {'orgs': orgs,
                   'orgs_rank': orgs_rank,
                   'num': num,
                   'sort': sort,
                   'ct': ct,
                   'citys': citys,
                   'city_id': city_id
                   }

        return render(request, 'org-list.html', context)


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


class OrgDetailView(View):
    def get(self, request, id, *args, **kwargs):
        # 未登录显示收藏，已登录根据实际是否收藏来显示
        user = request.user
        if not user.is_authenticated:
            fav_org = False
        else:
            user_fav_obj = UserFavorite.objects.filter(user=user, fav_id=int(id), fav_type=2)
            if user_fav_obj:
                fav_org = True
            else:
                fav_org = False

        # 机构详情查看，点击数加1
        org = CourseOrg.objects.get(id=int(id))
        org.click_num += 1
        org.save()

        # 显示机构课程前3条
        all_courses = org.courses_set.all()[:3]
        teachers = org.teachers_set.all()[:3]
        return render(request, 'org-detail-homepage.html',
                      {'org': org,
                       'all_courses': all_courses,
                       'teachers': teachers,
                       'fav_org': fav_org})


class OrgCoursesView(View):
    def get(self, request, id, *args, **kwargs):
        org = CourseOrg.objects.get(id=int(id))
        courses = org.courses_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses, request=request, per_page=1)
        courses = p.page(page)

        return render(request, 'org-detail-course.html', {'org': org, 'courses': courses})
