from django.db import models
from django.utils import timezone

from organizations.models import Teacher, CourseOrg


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"所属机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u"讲师", null=True, blank=True)

    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情', default='')
    is_banner = models.BooleanField(default=False, verbose_name='是否是轮播图')
    degree = models.CharField(max_length=20, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name=u'课程难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    you_need_know = models.CharField(max_length=300, default=u"一颗勤学的心是本课程必要前提", verbose_name=u"课程须知")
    teacher_tell = models.CharField(max_length=300, default=u"什么都可以学到,按时交作业,不然叫家长", verbose_name=u"老师告诉你")
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(max_length=20, verbose_name='课程类别', default='')
    tag = models.CharField(max_length=15, verbose_name='课程标签', default='')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'课程')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
