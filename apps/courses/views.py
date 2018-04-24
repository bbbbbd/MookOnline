# coding: utf-8
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequireMixin


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by('-click_nums')[:3]
        search_kw = request.GET.get('keywords')
        if search_kw:
            all_courses = all_courses.filter(Q(name__icontains=search_kw) | Q(desc__icontains=search_kw) | Q(datail__icontains=search_kw))

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-fav_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-syudents')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(~Q(id=int(course_id)), tag=tag).order_by('-click_nums')[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(LoginRequireMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.syudents += 1
        course.save()
        all_resources = CourseResource.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.user.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses
        })


class CommentView(LoginRequireMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #查询用户是否已经关联了本课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        all_resources = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.user.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comment': all_comment,
            'relate_courses': relate_courses
        })


class AddCommentView(View):
    def post(self, request):
        course_id = request.POST.get('course_id', 0)
        course = Course.objects.get(id=int(course_id))
        comment = request.POST.get('comments')
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        if int(course_id) and comment:
            add_comment = CourseComments()
            add_comment.user = request.user
            add_comment.course = course
            add_comment.comments = comment
            add_comment.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')