from django.db import models

# Create your models here.
class MessageInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name="用户名")
    email = models.EmailField(verbose_name="邮箱")
    address = models.CharField(max_length=255, verbose_name="地址")
    message = models.TextField(verbose_name="留言")

    # 元类
    class Meta:
        # 创建的表名称
        db_table = "message_info"
        # 后台显示名称
        verbose_name = "用户表单"
        verbose_name_plural = verbose_name
