import xadmin
from django.contrib.auth import get_user_model

UserProfile = get_user_model()

# 创建自己的ModelAdmin类
class UserCustomAdmin(object):
    pass

# admin.site.register(创建的模型类,创建的ModelAdmin)
xadmin.site.register(UserProfile, UserCustomAdmin)
