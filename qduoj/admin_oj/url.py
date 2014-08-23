#!/usr/bin/python
# coding=utf-8

from django.conf.urls import patterns, include, url
from admin_oj import views
from admin_oj import problem_views
from admin_oj import contest_views

urlpatterns = patterns('',
        url(r'^index/$', views.index, name='admin_index'),

        )
