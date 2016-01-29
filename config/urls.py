# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView
from mysuper.users import views
from mysuper.users.models import Department
from django_filters.views import FilterView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),
    
    url(r'^listDeps/$', FilterView.as_view(model=Department)),
    
     url(
        regex=r'^department$',
        view=views.DepartmentListView.as_view(),
        name='listdep'
    ),

    # URL pattern for the DepartmentRedirectView
 
    # URL pattern for the DepartmentDetailView
    url(
        regex=r'department(?P<name>[\w.@+-]+)/$',
        view=views.DepartmentDetailView.as_view(),
        name='department-detail'
    ),

    # URL pattern for the DepartmentUpdateView
    url(
        regex=r'^department~update/$',
        view=views.DepartmentUpdateView.as_view(),
        name='update'
    ),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include("mysuper.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permissin Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
