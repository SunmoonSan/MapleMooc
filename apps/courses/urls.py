#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-11 10:32
# @site  : https://github.com/SunmoonSan
from django.urls import path, include, re_path

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentListView, CourseAddCommentView

app_name='course'
urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),  # 登录
    path('list/', CourseListView.as_view(), name='course_list'),
    path('detail/<int:course_id>', CourseDetailView.as_view(), name='course_detail'),
    path('info/<int:course_id>', CourseInfoView.as_view(), name='course_info'),
    path('comment/<int:course_id>', CourseCommentListView.as_view(), name='course_comment_list'),
    path('add_comment', CourseAddCommentView.as_view(), name='course_add_comment')
]