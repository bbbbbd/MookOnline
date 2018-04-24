# -*- coding:utf-8 -*-
from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavsView, MyTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    url(r'^list/$', UserInfoView.as_view(), name='user_list'),
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    url(r'^myfavs/org/$', MyFavsView.as_view(), name='myfavs_org'),
    url(r'^myfavs/teacher/$', MyTeacherView.as_view(), name='myfavs_teacher'),
    url(r'^myfavs/course/$', MyFavCourseView.as_view(), name='myfavs_course'),
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]
