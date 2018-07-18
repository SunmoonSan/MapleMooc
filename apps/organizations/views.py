import json

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from pure_pagination import Paginator, PageNotAnInteger

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

        return render(request, 'org/teacher-detail.html', {
            'teacher': teacher,
            'teach_courses': teach_courses,
            'sorted_teacher': sorted_teacher,
        })


# 授课机构列表
class OrgView(View):

    def get(self, request):
        all_orgs = CourseOrg.objects.all()

        all_cities = CityDict.objects.all()

        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(
                name__icontains=search_keywords) | Q(
                desc__icontains=search_keywords) | Q(
                address__icontains=search_keywords
            ))

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')

        org_nums = all_orgs.count()
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 1, request=request)

        orgs = p.page(page)

        return render(request, 'org/org-list.html', {
            'all_orgs': orgs,
            'all_city': all_cities,
            'org_nums': org_nums,
            # 'city_id': city_id,
            # 'category': category,
            # 'hot_orgs': hot_orgs,
            # 'sort': sort,
            # 'search_keywords': search_keywords,
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
            # 'all_teacher': all_teachers,
        })


# 机构课程
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=org_id)
        all_courses = course_org.course_set.all()
        has_fav = False

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
