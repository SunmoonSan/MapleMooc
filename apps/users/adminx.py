#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-09 10:55
# @site  : https://github.com/SunmoonSan
import xadmin
from users.models import EmailVerifyRecord, Banner


class EmailVerifyRecordAdmin(object):
    # code = models.CharField(max_length=20, verbose_name=u'验证码')
    # email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    # send_type = models.CharField(choices=(('register', u'注册'), ('forget', u'找回密码')), max_length=20, verbose_name=u'类型')
    # send_time = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
