# -*- coding:utf-8 -*-
from django.conf.urls import url

from .views import CourseView, CourseDetailView, CourseInfoView, CommentView, AddCommentView

urlpatterns = [
    url(r'^list/$', CourseView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='info'),
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
]