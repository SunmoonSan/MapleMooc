#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 2018-07-10 15:02
# @site  : https://github.com/SunmoonSan
from django import forms
from captcha.fields import CaptchaField


# 登录表单
from users.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})  # 验证码


# 忘记密码表单
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})  # 验证码


class ActiveForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


# 重置密码表单
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# 用户头像表单
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


# 用户信息表单
class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nickname', 'gender', 'birthday', 'address', 'mobile']