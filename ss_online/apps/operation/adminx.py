import xadmin
from .models import Banner, UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse
# Register your models here.

class BannerAdmin(object):
    # 列表页显示字段
    list_display = ['title', 'image', 'url', 'index']
    # 支持搜索的字段
    search_fields = ['title']
    # 过滤筛选的字段
    list_filter = ['title']
    # 列表字段支持编辑
    list_editable = ['title', 'image', 'url']
    # 分页
    list_per_page = 10

class UserAskAdmin(object):
    # 列表页显示字段
    list_display = ['name', 'mobile', 'course_name']
    # 支持搜索的字段
    search_fields = ['name', 'mobile']
    # 过滤筛选的字段
    list_filter = ['name', 'mobile']
    # 列表字段支持编辑
    list_editable = ['name', 'mobile', 'course_name']
    # 分页
    list_per_page = 10

class CourseCommentAdmin(object):
    # 列表页显示字段
    list_display = ['user', 'course', 'comments']
    # 支持搜索的字段
    search_fields = ['comments']
    # 过滤筛选的字段
    list_filter = ['comments']
    # 列表字段支持编辑
    # list_editable = ['user', 'course', 'comments']
    # 分页
    list_per_page = 10

class UserFavoriteAdmin(object):
    pass

class UserMessageAdmin(object):
    # 列表页显示字段
    list_display = ['user', 'message', 'has_read']
    # 支持搜索的字段
    search_fields = ['message']
    # 过滤筛选的字段
    list_filter = ['message']
    # 列表字段支持编辑
    # list_editable = ['user', 'course', 'comments']
    # 分页
    list_per_page = 10

class UserCourseAdmin(object):
    # 列表页显示字段
    list_display = ['user', 'course']
    # 支持搜索的字段
    # search_fields = ['message']
    # 过滤筛选的字段
    # list_filter = ['message']
    # 列表字段支持编辑
    # list_editable = ['user', 'course', 'comments']
    # 分页
    list_per_page = 10

xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentAdmin)
# xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
# xadmin.site.register(UserCourse, UserCourseAdmin)