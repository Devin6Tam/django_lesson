from django.contrib import admin
from .models import CourseOrg, Citys, Teachers
# Register your models here.

class CityAdmin(admin.ModelAdmin):
    pass

class TeacherAdmin(admin.ModelAdmin):
    pass

class CourseOrgAdmin(admin.ModelAdmin):
    pass

admin.site.register(Citys, CityAdmin)
admin.site.register(Teachers, TeacherAdmin)
admin.site.register(CourseOrg, CourseOrgAdmin)