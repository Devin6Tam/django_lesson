from django.db import models


# Create your models here.

class User(models.Model):
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    password = models.CharField(max_length=16, verbose_name="密码")

    class Meta:
        db_table = "sys_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mobile
