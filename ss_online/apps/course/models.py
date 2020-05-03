from django.db import models
from apps.user.models import BaseModel
from apps.organization.models import Teachers, CourseOrg
# Create your models here.

# 课程表
class Courses(BaseModel):
    # on_delete=models.CASCADE 当关联表中的数据删除时，这条数据也删除
    tearcher = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name='课程老师')
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='课程机构')
    name = models.CharField(max_length=200, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程简介')
    degree = models.CharField(max_length=6, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name='难度')
    learn_time = models.IntegerField(default=0, verbose_name='学习时长')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    category = models.CharField(max_length=20, default='后端开发', verbose_name='学习类别')
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='点击人数')
    youneed_know = models.CharField(max_length=200, default='', verbose_name='课程须知')
    tearcher_tell = models.CharField(max_length=200, default='', verbose_name='老师告诉你')
    detail = models.CharField(max_length=300, default='', verbose_name='课程详情')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='课程封面')
    course_fee = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='课程费用')
    is_classic = models.BooleanField(default=False, verbose_name='是否经典')

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 课程章节
class Lessons(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="课程名称")
    name = models.CharField(max_length=50, verbose_name="章节名称")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长")

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 学习视频
class Videos(BaseModel):
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, verbose_name="章节名称")
    name = models.CharField(max_length=100, verbose_name='视频名称')
    learn_time = models.IntegerField(default=0, verbose_name='学习时长')
    url = models.CharField(max_length=200, verbose_name='视频地址')

    class Meta:
        verbose_name = '学习视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 课程资源信息（资源下载地址）
class CourseSource(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="课程名称")
    name = models.CharField(max_length=100, verbose_name="名称")
    file = models.FileField(upload_to='courses/%Y/%m', verbose_name='下载地址')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name