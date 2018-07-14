#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-11 10:32
# @site  : https://github.com/SunmoonSan
from django.urls import path, include, re_path

from courses.views import CourseListView
from users.views import LoginView

app_name='course'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # 登录
    path('list/', CourseListView.as_view(), name='course_list'),
]