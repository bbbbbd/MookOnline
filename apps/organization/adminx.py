# -*- coding:utf-8 -*-
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CiytDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

xadmin.site.register(CityDict, CiytDictAdmin)


class CourseOrgAdmin(object):
    list_display = ['name', 'category', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'category', 'click_nums', 'fav_nums', 'address', 'city']
    list_filter = ['name', 'category', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    relfield_style = 'fk-ajax'


xadmin.site.register(CourseOrg, CourseOrgAdmin)


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'fav_nums', 'click_nums']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'fav_nums', 'click_nums', 'add_time']


xadmin.site.register(Teacher, TeacherAdmin)