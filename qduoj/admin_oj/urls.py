#!/usr/bin/python
# coding=utf-8

from django.conf.urls import patterns, include, url
from admin_oj import views, problem_views, contest_views, check_views
from admin_oj import news_views

urlpatterns = patterns('',
        url(r'^log/$', views.log, name='log'),
        url(r'^login/$', views.sign_in, name='log'),
        url(r'^logout/$', views.sign_out, name='log'),
        url(r'^index/$', views.index, name='problem_index'),
        url(r'^admin_logout/$', views.sign_out, name='admin_lokout'),
        url(r'^get_problem_list/$', problem_views.get_problem_list, name=''),
        url(r'^problem_add/$', problem_views.problem_add, name=''),
        url(r'^problem_fix/$', problem_views.problem_fix, name=''),
        url(r'^problem_get/$', problem_views.problem_get, name=''),
        url(r'^problem_visible/$', problem_views.problem_visible, name=''),
        url(r'^problem_update/$', problem_views.problem_update, name=''),
       
        url(r'^problem_rejudge/$', problem_views.problem_rejudge, name=''),
        url(r'^solution_rejudge/$', problem_views.solution_rejudge, name=''),
        url(r'^get_contest_list/$', contest_views.get_contest_list, name=''),
        url(r'^get_contest_sim/$', contest_views.get_contest_sim, name=''),
        url(r'^get_sim_code/$', contest_views.get_sim_code, name=''),
        url(r'^contest_add/$', contest_views.contest_add, name=''),
        url(r'^contest_get/$', contest_views.contest_get, name=''),
        url(r'^contest_fix/$', contest_views.contest_fix, name=''),
        url(r'^contest_visible/$', contest_views.contest_visible, name=''),

        url(r'^get_check_list/$', check_views.get_check_list, name=''),
        url(r'^check_save/$', check_views.check_save, name=''),
        url(r'^get_news_list/$', news_views.get_news_list, name=''),
        url(r'^news_add/$', news_views.news_add, name=''),
        url(r'^news_delete/$', news_views.news_delete, name=''),
        url(r'^news_get/$', news_views.news_get, name=''),
        url(r'^news_modify/$', news_views.news_modify, name=''),
        url(r'^news_visible/$', news_views.news_visible, name=''),
        url(r'^news_show/$', news_views.news_show, name='news_show'),

        )
