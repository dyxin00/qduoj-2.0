#!/usr/bin/python
# coding=utf-8

from django.conf.urls import patterns, include, url
from admin_oj import views, problem_views, contest_views

urlpatterns = patterns('',
        url(r'^index/$', views.index, name='problem_index'),
        url(r'^admin_logout/$', views.sign_out, name='admin_lokout'),
        url(r'^get_problem_list/$', problem_views.get_problem_list, name=''),
        url(r'^problem_add/$', problem_views.problem_add, name=''),
        url(r'^problem_get/$', problem_views.problem_get, name=''),
        url(r'^problem_visible/$', problem_views.problem_visible, name=''),
        
        url(r'^get_contest_list/$', contest_views.get_contest_list, name=''),
        )
