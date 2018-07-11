#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-11 10:40
# @site  : https://github.com/SunmoonSan
from django.urls import path

from .views import OrgView

app_name = 'org'
urlpatterns = [
    path('org_list/', OrgView.as_view(), name='org_list')
]