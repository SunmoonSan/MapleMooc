from django.db import models

# Create your models here.
from courses.models import Course
from users.models import UserProfile


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name


class CourseMoments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name=u'评论')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name


# 用户收藏表
class  UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户', on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '课程机构'), (3, '讲师')), default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'收藏时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})收藏了{1}'.format(self.user, self.fav_type)


# 用户消息表
class UserMessage(models.Model):
    # user为整型, 为0就群发所有用户, 不为0就发给对应id的用户
    user = models.IntegerField(default=0, verbose_name=u'接收用户')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})接收了{1}'.format(self.user, self.message)


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name
