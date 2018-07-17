#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-11 10:32
# @site  : https://github.com/SunmoonSan
from django.views.static import serve
from django.urls import path, include, re_path
from django.views.generic import TemplateView

import xadmin
from MapleMooc.settings import MEDIA_ROOT
from users.views import LoginView, ForgetPwdView, ResetView, ModifyPwdView, RegisterView, ActiveUserView, IndexView, \
    LogoutView, UserInfoView, UploadImageView, UpdatePwdView, MyCourseView, MyMessageView

app_name = 'user'
urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),  # 登录
    path('logout/', LogoutView.as_view(), name='logout'),  # 退出
    path('register/', RegisterView.as_view(), name='register'),  # 注册
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    path('reset/', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 上传用户头像
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    path('my_course/', MyCourseView.as_view(), name='my_course'),  # 我的课程
    path('my_message/', MyMessageView.as_view(), name='my_message'),  # 我的消息
    path('xadmin/', xadmin.site.urls),
    path('active/<active_code>/', ActiveUserView.as_view(), name='user_active'),

]
