from django.contrib import admin
from .models import Banner, UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse
# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    pass

class UserAskAdmin(admin.ModelAdmin):
    pass

class CourseCommentAdmin(admin.ModelAdmin):
    pass

class UserFavoriteAdmin(admin.ModelAdmin):
    pass

class UserMessageAdmin(admin.ModelAdmin):
    pass

class UserCourseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Banner, BannerAdmin)
admin.site.register(UserAsk, UserAskAdmin)
admin.site.register(CourseComments, CourseCommentAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(UserCourse, UserCourseAdmin)