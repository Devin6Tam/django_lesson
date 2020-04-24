from django.contrib import admin
from .models import Courses, Lessons, Videos,CourseSource
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    pass

class LessonAdmin(admin.ModelAdmin):
    pass

class VideoAdmin(admin.ModelAdmin):
    pass

class CourseSourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Courses, CourseAdmin)
admin.site.register(Lessons, LessonAdmin)
admin.site.register(Videos, VideoAdmin)
admin.site.register(CourseSource, CourseAdmin)