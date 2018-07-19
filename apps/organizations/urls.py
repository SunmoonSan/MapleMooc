#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-11 10:40
# @site  : https://github.com/SunmoonSan
from django.urls import path

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, TeacherListView, \
    TeacherDetailView, AddFavoriteView

app_name = 'org'
urlpatterns = [
    # 教师栏列表
    path('teacher_list/', TeacherListView.as_view(), name='teacher_list'),
    # 教师详情页
    path('teacher_detail/<int:teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),
    # 机构列表
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    # home页面,取纯数字
    path('home/<int:org_id>/', OrgHomeView.as_view(), name="org_home"),
    # 访问课程
    path('course/<int:org_id>/', OrgCourseView.as_view(), name="org_course"),
    # 机构介绍
    path('desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    # 机构教师
    path('teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),
    # 添加收藏
    path('add_fav/', AddFavoriteView.as_view(), name='add_favorite'),

]
