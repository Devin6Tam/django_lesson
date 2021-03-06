from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


# Create your models here.

class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女')
    )
    nick_name = models.CharField(max_length=200, verbose_name='昵称', null=True, blank=True)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=300, verbose_name='地址', default='')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    image = models.ImageField(upload_to='head_image/%Y/%m', default='default.jpg', verbose_name='头像')

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def msg_not_read(self):
        return self.usermessage_set.filter(has_read=False).count()
