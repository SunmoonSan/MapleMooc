"""MapleMooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from organizations.views import OrgView
from MapleMooc.settings import MEDIA_ROOT

from users.views import LoginView, ActiveUserView, RegisterView, ForgetPwdView, ResetView, ModifyPwdView, IndexView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='user/index.html'), name='index'),
    path('', IndexView.as_view(), name='index'),
    path('user/', include('users.urls')),
    path('org/', include('organizations.urls')),
    # 配置上传文件的访问处理
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # path('login/', LoginView.as_view(), name='login'),  # 登录
    # path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    # path('reset/', ResetView.as_view(), name='reset_pwd'),
    # path('reset/', ModifyPwdView.as_view(), name='modify_pwd'),
    # path('register/', RegisterView.as_view(), name='register'),  # 注册
    path('xadmin/', xadmin.site.urls),
    # path('captcha/', include('captcha.urls')),  # 验证码
    # path('active/<active_code>/', ActiveUserView.as_view(), name='user_active'),

]
