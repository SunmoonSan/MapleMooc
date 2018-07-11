#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-10 21:34
# @site  : https://github.com/SunmoonSan
from random import Random

from django.core.mail import send_mail, EmailMessage

from users.models import EmailVerifyRecord
from MapleMooc.settings import EMAIL_FROM


def generate_random_str(randomlength):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'Maple慕课网注册激活链接'
        email_body = '请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{}'.format(code)

        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        status = msg.send()
        # status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if status:
            pass

    elif send_type == 'forget':
        email_title = 'Maple慕课网密码重置激活链接'
        email_body = '请点击下面的链接激活你的账号: http://127.0.0.1:8000/reset/{}'.format(code)

        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        status = msg.send()
        if status:
            pass
