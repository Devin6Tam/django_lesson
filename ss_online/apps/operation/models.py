from django.db import models
from django.contrib.auth import get_user_model
from apps.user.models import BaseModel
from apps.course.models import Courses

# Create your models here.

UserProfile = get_user_model()


# 轮播图展览
class Banner(BaseModel):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="bannel/%Y/%m", max_length=200, verbose_name="链接图片")
    url = models.CharField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=0, verbose_name="顺序")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 立即咨询
class UserAsk(BaseModel):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    course_name = models.CharField(max_length=50, verbose_name="课程名")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{name}_{course}({mobile})".format(name=self.name, course=self.course_name, mobile=self.mobile)


# 评论
class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="课程")
    comments = models.CharField(max_length=200, verbose_name="评论内容")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comments


# 收藏
class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(verbose_name="数据")
    fav_type = models.IntegerField(choices=((1, "课程"), (2, "课程机构"), (3, "讲师")), default=1, verbose_name="收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{user}_{id}".format(user=self.user.username, id=self.fav_id)


# 用户信息
class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    message = models.CharField(max_length=200, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


# 用户课程
class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.name
