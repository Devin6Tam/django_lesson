import xadmin
from .models import Banner, UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse
# Register your models here.

class BannerAdmin(object):
    pass

class UserAskAdmin(object):
    pass

class CourseCommentAdmin(object):
    pass

class UserFavoriteAdmin(object):
    pass

class UserMessageAdmin(object):
    pass

class UserCourseAdmin(object):
    pass

xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)