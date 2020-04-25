import xadmin
from .models import CourseOrg, Citys, Teachers
# Register your models here.

class CityAdmin(object):
    pass

class TeacherAdmin(object):
    pass

class CourseOrgAdmin(object):
    pass

xadmin.site.register(Citys, CityAdmin)
xadmin.site.register(Teachers, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)