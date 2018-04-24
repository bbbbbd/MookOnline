# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile (AbstractUser):
    nick_name = models.CharField('昵称', max_length=50, default='')
    birday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', choices=(
        ('male', '男'), ('female', '女')), default='male', max_length=6)
    address = models.CharField('地址', max_length=100, default='')
    mobile = models.CharField('手机', max_length=11, null=True, blank=True)
    image = models.ImageField(
        '头像',
        upload_to='image/%Y/%m',
        default='image/default.png',
        max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField('验证码类型', choices=(
        ('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')), max_length=30)
    send_time = models.DateField('发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{}({})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='banner/%Y/%m', max_length=100)
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
