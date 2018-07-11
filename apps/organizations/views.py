from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View


# 课程机构列表功能
from organizations.models import CourseOrg, CityDict

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class OrgView(View):

    def get(self, request):
        all_orgs = CourseOrg.objects.all()

        all_cities = CityDict.objects.all()
        print(all_orgs, all_cities)

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

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_city': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'search_keywords': search_keywords,
        })
