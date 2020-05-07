from django.db import models
from apps.user.models import BaseModel


# Create your models here.

class Citys(BaseModel):
    name = models.CharField(max_length=50, verbose_name='城市名称')
    desc = models.TextField(verbose_name='城市描述')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 机构
class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='课程简介')
    tag = models.CharField(max_length=10, default='全国知名', verbose_name='机构标签')
    categroy = models.CharField(verbose_name='机构类别', max_length=4,
                                choices=(('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')))
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='点击人数')
    address = models.CharField(max_length=300, verbose_name='机构地址', default='')
    students = models.IntegerField(default=0, verbose_name='学生人数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='机构logo')
    course_num = models.IntegerField(default=0, verbose_name='课程数')
    city = models.ForeignKey(Citys, verbose_name='所在城市', on_delete=models.CASCADE)
    is_auth = models.BooleanField(default=False, verbose_name='是否认证')
    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')

    # 筛选机构的经典课程
    def courses(self):
        return self.courses_set.filter(is_classic=True)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 机构课程数
    def course_nums(self):
        return self.courses_set.all().count()

    # 机构讲师人数
    def teacher_nums(self):
        return self.teachers_set.all().count()


# 机构讲师
class Teachers(BaseModel):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所在机构')
    name = models.CharField(max_length=50, verbose_name='讲师名称')
    age = models.IntegerField(default=20, verbose_name='年龄')
    work_year = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, default='班主任', verbose_name='工作岗位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='点击人数')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像')
    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')

    class Meta:
        verbose_name = '讲师信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_num(self):
        # return len(self.courses_set.all())
        return self.courses_set.all().count()