# coding: utf-8
"""MookOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, LogoutViem, ForgetViem, ResetView, ModifypwdView
from MookOnline.settings import MEDIA_ROOT
from users.views import IndexView, page_not_found, server_error

urlpatterns = [
    url(r'^$', IndexView.as_view(),  name='index'),

    url(r'^login/$', LoginView.as_view(),  name='login'),
    url(r'^register/$', RegisterView.as_view(), name='regiser'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^logout/$', LogoutViem.as_view(), name='logout'),
    url(r'^forget/$', ForgetViem.as_view(), name='forget_pwd'),
    url(r'^modifypwd/$', ModifypwdView.as_view(), name='modify_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),

    url(r'^org/', include('organization.urls', namespace='org')),

    url(r'^course/', include('courses.urls', namespace='course')),

    url(r'^users/', include('users.urls', namespace='users')),
    # 静态文件
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^xadmin/', xadmin.site.urls),
]

#全局404配置
handler404 = page_not_found

#全局500错误
handler500 = server_error