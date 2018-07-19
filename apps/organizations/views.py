import json

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operations.models import UserFavorite
from organizations.forms import UserAskForm
from organizations.models import CourseOrg, CityDict, Teacher


# 授课教师
class TeacherListView(View):

    def get(self, request):
        all_teacher = Teacher.objects.all()
        sort = request.GET.get('sort', '')

        if sort and sort == 'hot':
            all_teacher = all_teacher.order_by('click_nums')

        sorted_teacher = Teacher.objects.all().order_by('click_nums')[:3]  # 人气前3位

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_teacher, 1, request=request)
        teachers = p.page(page)

        return render(request, 'org/teachers-list.html', {
            'teachers': teachers,
            'sorted_teacher': sorted_teacher,
            'sort': sort,
        })


# 教师详情页
class TeacherDetailView(View):

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        teacher.click_nums += 1  # 点击量加1
        teacher.save()

        teach_courses = teacher.course_set.all()  # 该老师所教课程

        sorted_teacher = Teacher.objects.all().order_by('click_nums')[:3]  # 人气前3位

        has_fav_teacher = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_fav_teacher = True

        has_fav_org = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_fav_org = True

        return render(request, 'org/teacher-detail.html', {
            'teacher': teacher,
            'teach_courses': teach_courses,
            'sorted_teacher': sorted_teacher,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org
        })


# 添加收藏页
class AddFavoriteView(View):
    """
    :type 1 课程, 2 课程机构 3 授课讲师
    """
    def post(self, request):

        favorite_id = request.POST.get('fav_id', 0)
        favorite_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({
                'status': 'fail',
                'msg': '用户未登录!'
            }), content_type='application/json')

        favorite = UserFavorite.objects.filter(user=request.user, fav_id=favorite_id, fav_type=favorite_type)

        if favorite:  # favorite非空, 取消收藏
            favorite.delete()

            if favorite_type == '1':
                course = Course.objects.get(pk=int(favorite_id))
                course.fav_num -= 1
                if course.fav_num < 0:
                    course.fav_num = 0
                course.save()

            elif favorite_type == '2':  # 课程机构
                course_org = CourseOrg.objects.get(pk=int(favorite_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()

            elif favorite_type == '3':  # 授课教师
                teacher = Teacher.objects.get(pk=int(favorite_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse(json.dumps({
                'status': 'success',
                'msg': '收藏'
            }), content_type='application/json')
        else:  # favorite为空, 添加收藏
            favorite = UserFavorite()
            if int(favorite_type) > 0 and int(favorite_id) > 0:
                favorite.fav_id = int(favorite_id)
                favorite.fav_type = int(favorite_type)
                favorite.user = request.user
                favorite.save()

                if favorite_type == '1':
                    course = Course.objects.get(pk=int(favorite_id))
                    course.fav_num += 1
                    course.save()
                elif favorite_type == '2':  # 课程机构
                    course_org = CourseOrg.objects.get(pk=int(favorite_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif favorite_type == '3':  # 授课教师
                    teacher = Teacher.objects.get(pk=int(favorite_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse(json.dumps({
                    'status': 'success',
                    'msg': '已收藏'
                }), content_type='application/json')
            else:
                return HttpResponse(json.dumps({
                    'status': 'success',
                    'msg': '收藏出错!'
                }), content_type='application/json')


# 授课机构列表
class OrgView(View):

    def get(self, request):
        all_orgs = CourseOrg.objects.all()  # 所有课程

        all_cities = CityDict.objects.all()  # 所以城市

        hot_orgs = all_orgs.order_by('-click_nums')[:3]  # 热门机构

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(
                name__icontains=search_keywords) | Q(
                desc__icontains=search_keywords) | Q(
                address__icontains=search_keywords
            ))

        city_id = request.GET.get('city', '')  # 针对城市过滤
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')  # 针对类比过滤
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')  # 排序
        if sort:
            if sort == 'students':  # 学习人数
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':  # 课程数
                all_orgs = all_orgs.order_by('-course_nums')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        org_nums = all_orgs.count()
        p = Paginator(all_orgs, 1, request=request)

        orgs = p.page(page)

        return render(request, 'org/org-list.html', {
            'all_orgs': orgs,
            'all_city': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'search_keywords': search_keywords,
        })


# 用户添加咨询
class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse(json.dumps({
                'status': 'success',

            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'status': 'fail',
                'msg': '添加出错!'
            }), content_type='application/json')


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1  # 点击加1
        course_org.save()
        all_courses = course_org.course_set.all()[:4]
        all_teachers = course_org.teacher_set.all()

        return render(request, 'org/org-detail-homepage.html', {
            'course_org': course_org,
            'all_course': all_courses,
            'all_teacher': all_teachers,
        })


# 机构课程
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'

        course_org = CourseOrg.objects.get(id=org_id)
        all_courses = course_org.course_set.all()

        has_fav = False
        if request.user.is_authenticated and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            has_fav = True

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org/org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


# 机构介绍
class OrgDescView(View):
    def get(self, request, org_id):
        # current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        # if request.user.is_authenticated:
        #     if UserFavorite.objects.filter(us)

        return render(request, 'org/org-detail-desc.html', {
            'course_org': course_org,
            # 'current_page': current_page,
        })


# 机构讲师
class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        all_teachers = course_org.teacher_set.all()

        return render(request, 'org/org-detail-teachers.html', {
            'course_org': course_org,
            'all_teachers': all_teachers,

        })
