# coding: utf-8
import json

from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ResetForm, UploadImageForm, ModifyPwdForm, UploadInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequireMixin
from operation.models import UserCourse, UserFavorite
from organization.models import CourseOrg, Teacher
from courses.models import Course


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在！'})
            else:
                password = request.POST.get('password')
                user = UserProfile.objects.create(username=email, is_active=False, email=email,
                                                  password=make_password(password))
                user.save()
                send_register_email(email, 'register')
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutViem(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class ForgetViem(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            if UserProfile.objects.filter(email=email):
                send_register_email(email, 'forget')
            else:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '用户不存在！'})
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifypwdView(View):
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            if password != password2:
                return render(request, 'password_reset.html', {'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email')
            return render(request, 'password_reset.html', {'reset_form': reset_form, 'email': email})


class UserInfoView(LoginRequireMixin, View):
    def get(self, request):
        site = 'my_info'
        return render(request, 'usercenter-info.html', {'site': site})

    def post(self, request):
        info_form = UploadInfoForm(request.POST, instance=request.user)
        if info_form.is_valid():
            info_form.save()
            return HttpResponse('{"status": "sucess"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(info_form.errors), content_type='application/json')


class UploadImageView(LoginRequireMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data.get('image')
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse('{"status": "sucess"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdatePwdView(LoginRequireMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password != password2:
                return HttpResponse('{"status": "fail", "msg": "密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(password)
            user.save()

            return HttpResponse('{"status": "sucess"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequireMixin, View):
    def get(self, request):
        email = request.GET.get('email')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已被注册"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequireMixin, View):
    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequireMixin, View):
    def get(self, request):
        site = 'my_course'
        user_course = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'site': site,
            'user_course': user_course
        })


class MyFavsView(LoginRequireMixin, View):
    def get(self, request):
        user_favs = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            user_favs.append(org)
        site = 'my_collect'
        return render(request, 'usercenter-fav-org.html', {
            'site': site,
            'user_favs': user_favs,
        })


class MyTeacherView(LoginRequireMixin, View):
    def get(self, request):
        user_favs = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            user_favs.append(teacher)
        site = 'my_collect'
        return render(request, 'usercenter-fav-teacher.html', {
            'site': site,
            'user_favs': user_favs,
        })


class MyFavCourseView(LoginRequireMixin, View):
    def get(self, request):
        user_favs = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            user_favs.append(course)
        site = 'my_collect'
        return render(request, 'usercenter-fav-course.html', {
            'site': site,
            'user_favs': user_favs,
        })


class MyMessageView(LoginRequireMixin, View):
    def get(self, request):
        site = 'my_message'
        return render(request, 'usercenter-message.html', {
            'site': site,
        })


class IndexView(View):
    def get(self, request):
        # 轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:2]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


# 404
def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 500
def server_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
