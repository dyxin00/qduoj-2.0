#!/usr/bin/python
# coding=utf-8

from django.conf.urls import patterns, include, url
from admin_oj import views

urlpatterns = patterns('',
        url(r'^index/$', views.index, name='problem_index'),

        )
