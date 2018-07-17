#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-17 23:02
# @site  : https://github.com/SunmoonSan
import xadmin

from operations.models import UserMessage


class UserMessageAdmin:
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


xadmin.site.register(UserMessage, UserMessageAdmin)