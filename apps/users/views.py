import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.urls import reverse
from django.views.generic import View
from pure_pagination import Paginator

from courses.models import Course
from operations.models import UserCourse, UserMessage, UserFavorite
from organizations.models import CourseOrg, Teacher
from users.models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, ActiveForm, UserInfoForm, UploadImageForm
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 支持email登录
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登录
class LoginView(View):

    def get(self, request):
        redirect_url = request.GET.get('next', '')
        return render(request, 'user/login.html', {
            'redirect_url': redirect_url,
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            _username = request.POST.get('username', '')
            _password = request.POST.get('password', '')
            user = auth.authenticate(username=_username, password=_password)
            if user is not None:
                if user.is_active:  # 判断是否已激活
                    auth.login(request, user)
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    return HttpResponseRedirect(reverse("index"))  # 跳转到首页
                    # return render(request, 'index.html')
                else:
                    return render(request, 'user/login.html', {'msg': '邮箱尚未激活,请进入邮箱激活!'})
            else:
                return render(request, 'user/login.html', {'msg': '用户名或密码错误!'})
        else:
            render(request, 'user/login.html', {'login_form': login_form})


# 退出
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('index'))


# 激活邮箱
class ActiveUserView(View):

    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'user/login.html')


# 注册
class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')

            if UserProfile.objects.filter(email=username):
                return render(request, 'user/register.html', {
                    'register_form': register_form,
                    'msg': '用户已经存在了!'
                })

            password = request.POST.get('password', '')

            userprofile = UserProfile()
            userprofile.username = username
            userprofile.email = username
            userprofile.is_active = True  # 未激活
            userprofile.password = make_password(password=password)  # 加密
            userprofile.save()

            # 发送激活邮件
            # send_register_email(username, 'register')  阿里云禁用邮箱25端口
            return render(request, 'user/login.html')  # 跳转到登录页面
        else:
            return render(request, 'user/register.html', {'register_form': register_form})


# 忘记密码
class ForgetPwdView(View):

    def get(self, request):
        active_form = ForgetForm()
        return render(request, 'user/forgetpwd.html', {
            'active_form': active_form,
        })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.data.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'user/forgetpwd.html', {'forget_form': forget_form})


# 重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)

        active_form = ActiveForm()
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'user/password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')

        return render(request, 'user/login.html')


# 修改密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = modify_form.data.get('password1', '')
            pwd2 = modify_form.data.get('password2', '')
            active_code = modify_form.data.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'user/password_reset.html', {'email': active_code, 'msg': '密码不一致'})

            all_record = EmailVerifyRecord.objects.filter(code=active_code)
            for record in all_record:
                email = record.email
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'user/login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'user/password_reset.html', {'email': email, 'modify_form': modify_form})


# 用户信息
class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'user/usercenter-info.html')

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps({
                'status': 'success'
            }), content_type='application/json')

        return render(request, 'user/index.html')


# 上传用户头像
class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/user/login'

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)

        if image_form.is_valid():
            image_form.save()
            return HttpResponse(json.dumps({
                'status': 'success'
            }), content_type='application/json')

        else:
            return HttpResponse(json.dumps({
                'status': 'fail'
            }), content_type='application/json')


# 个人中心修改密码
class UpdatePwdView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/user/login'

    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')

            if pwd1 != pwd2:
                return HttpResponse(json.dumps({
                    'status': 'fail',
                    'msg': '密码不一致!'
                }), content_type='application/json')

            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse(json.dumps({
                'status': 'success'
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_pwd_form.errors),
                                content_type='application/json')


# 我的课程
class MyCourseView(LoginRequiredMixin, View):

    def get(self, request):
        user_course = UserCourse.objects.filter(user=request.user)
        return render(request, 'user/usercenter-mycourse.html', )


class MyFavoriteView(LoginRequiredMixin, View):
    def get(self, request):
        fav_type = request.GET.get('fav_type', 1)

        if fav_type == '2':  # 收藏课程机构
            favorite_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)

            orgs = []
            for org in favorite_orgs:
                o = CourseOrg.objects.get(pk=org.fav_id)
                orgs.append(o)
            return render(request, 'user/usercenter-fav-org.html', {
                'orgs': orgs
            })
        elif fav_type == '3':  # 收藏授课教师
            favorite_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)

            teachers = []
            for teacher in favorite_teachers:
                t = Teacher.objects.get(pk=teacher.fav_id)
                teachers.append(t)
            return render(request, 'user/usercenter-fav-teacher.html', {
                'teachers': teachers,
            })

        favorite_course = UserFavorite.objects.filter(user=request.user, fav_type=1)

        courses = []
        for course in favorite_course:
            c = Course.objects.get(pk=course.fav_id)
            courses.append(c)
        return render(request, 'user/usercenter-fav-course.html', {
            'courses': courses
        })


# 我的消息
class MyMessageView(LoginRequiredMixin, View):

    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)  # user是整形id
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for message in all_unread_message:
            message.has_read = True
            message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4)
        messages = p.page(page)
        return render(request, 'user/usercenter-message.html', {
            'messages': messages
        })


# 网站首页
class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')[:5]  # 轮播图
        # 正常位课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播图课程取三个
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'user/index.html', {
            "all_banner": all_banner,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })
