#!/usr/bin/python
# coding=utf-8

from django.conf.urls import patterns, include, url
from admin_oj import views

urlpatterns = patterns('',
        url(r'^index/$', views.index, name='problem_index'),
        url(r'^admin_logout/$', views.sign_out, name='admin_logout'),
        url(r'^get_problem_list/$', views.get_problem_list, name=''),
        url(r'^problem_visible/$', views.problem_visible, name=''),

        )
