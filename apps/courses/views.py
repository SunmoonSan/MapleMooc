import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator

from operations.models import CourseMoments, UserFavorite
from .models import Course, Video


# 课程列表
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:2]
        # 分类排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course/course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []

        has_fav_course = False  # 收藏课程
        has_fav_org = False  # 收藏机构

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course/course-detail.html', {
            'course': course,
            'relate_coursers': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        return render(request, 'course/course-video.html', {
            'course': course,

        })


class CourseCommentListView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseMoments.objects.filter(course_id=course_id).order_by('-add_time')

        return render(request, 'course/course-comment.html', {
            'course': course,
            'all_comments': all_comments,
        })


class CourseAddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({
                'status': 'fail',
                'msg': '用户未登录',
            }), content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comment_content = request.POST.get('comments', '')

        if int(course_id) > 0 and comment_content:
            course_comment = CourseMoments()

            course = Course.objects.get(id=int(course_id))

            course_comment.course = course
            course_comment.comments = comment_content
            course_comment.user = request.user
            course_comment.save()

            return HttpResponse(json.dumps({
                'status': 'success',
                'msg': '评论成功!'
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'status': 'fail',
                'msg': '评论失败!',
            }), content_type='application/json')


class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        # print('video_id', video_id)
        video = Video.objects.get(id=video_id)
        # print(video)
        course = video.lesson.course
        # print(course)
        return render(request, 'course/course-play.html', {
            'course': course,
        })









