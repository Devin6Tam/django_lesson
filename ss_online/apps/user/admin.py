from django.contrib import admin
# from .models import UserProfile
# 导入对应的模型类
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# Register your models here.

UserProfile = get_user_model()

# 创建自己的ModelAdmin类
class UserCustomAdmin(UserAdmin):
    pass

# admin.site.register(创建的模型类,创建的ModelAdmin)
admin.site.register(UserProfile, UserCustomAdmin)
