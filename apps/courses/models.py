# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(
        CourseOrg,
        verbose_name='课程机构',
        null=True,
        blank=True)
    name = models.CharField('课程名', max_length=50)
    desc = models.CharField('描述', max_length=300)
    datail = models.TextField('课程详情')
    is_banner = models.BooleanField('是否轮播', default=False)
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    degree = models.CharField('课程难度', choices=(
        ('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=4)
    lenrn_times = models.IntegerField('学习时长', default=0)
    syudents = models.IntegerField('学习人数', default=0)
    fav_nums = models.IntegerField('收藏数', default=0)
    image = models.ImageField('封面片', upload_to='courses/%Y/%m', max_length=100)
    click_nums = models.IntegerField('点击量', default=0)
    category = models.CharField('课程类别', max_length=20, null=True, blank=True)
    tag = models.CharField('课程标签', max_length=20, null=True, blank=True)
    you_need_know = models.CharField('课程须知',max_length=300, default='')
    teacher_tell_you = models.CharField('老师建议', max_length=300, default='')
    add_time = models.DateField('添加时间', default=datetime.now)

    # 获取课程章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    # 获取学习这门课程的用户
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_lessons(self):
        return self.lesson_set.all()

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField('章节名', max_length=100)
    add_time = models.DateField('添加时间', default=datetime.now)

    def get_videos(self):
        return self.video_set.all()

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField('视频名', max_length=100)
    add_time = models.DateField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField('名称', max_length=100)
    download = models.FileField(
        '资源文件',
        upload_to='courses/resource/%Y/%m',
        max_length=100)
    add_time = models.DateField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
