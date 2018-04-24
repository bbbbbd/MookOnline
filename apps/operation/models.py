# coding: utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course


class UserAsk(models.Model):
    name = models.CharField('姓名', max_length=20)
    mobile = models.CharField('手机', max_length=11)
    course_name = models.CharField('课程名', max_length=50)
    add_time = models.DateField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseComments(models.Model):
    '''
    课程评论
    '''
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    comments = models.CharField('评论', max_length=200)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return unicode(self.user)


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField('数据ID', default=0)
    fav_type = models.IntegerField('收藏类型', choices=(
        (1, '课程'), (2, '课程机构'), (3, '讲师')), default=1)
    add_time = models.DateField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return unicode(self.user)


class UserMessage(models.Model):
    user = models.IntegerField('接受用户', default=0)
    message = models.CharField('消息内容', max_length=500)
    has_read = models.BooleanField('是否已读', default=False)
    add_time = models.DateField('发送时间', default=datetime.now)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateField('学习时间', default=datetime.now)

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}-{1}'.format(self.user, self.course)
