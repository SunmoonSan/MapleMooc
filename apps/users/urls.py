#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-11 10:32
# @site  : https://github.com/SunmoonSan
from django.views.static import serve
from django.urls import path, include, re_path
from django.views.generic import TemplateView

import xadmin
from MapleMooc.settings import MEDIA_ROOT
from users.views import LoginView, ForgetPwdView, ResetView, ModifyPwdView, RegisterView, ActiveUserView, IndexView

app_name='user'
urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),  # 登录
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    path('reset/', ResetView.as_view(), name='reset_pwd'),
    path('reset/', ModifyPwdView.as_view(), name='modify_pwd'),
    path('register/', RegisterView.as_view(), name='register'),  # 注册
    path('xadmin/', xadmin.site.urls),
    path('captcha/', include('captcha.urls')),  # 验证码
    path('active/<active_code>/', ActiveUserView.as_view(), name='user_active'),

]