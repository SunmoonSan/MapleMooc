#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-09 23:55
# @site  : https://github.com/SunmoonSan
import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin:
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'click_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'add_time', 'address', 'city']


class TeacherAdmin:
    list_display = ['org', 'name', 'work_years', 'work_company', 'desc', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'desc']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'desc', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
