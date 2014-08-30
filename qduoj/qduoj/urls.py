from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qduoj.views.home', name='home'),
    # url(r'^qduoj/', include('qduoj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),
#    url(r'^admin_oj/', include('admin_oj.urls')),
    url(r'^problem_index/$', 'problem.views.index', name='problem_index'),
    url(r'^problem/$', 'problem.views.problem', name='problem'),
    url(r'^submit_code/$', 'problem.views.submit_code', name='submit_code'),

    url(r'^$', 'oj_user.views.index', name='index'),
    url(r'^index/$', 'oj_user.views.index', name='index'),
    url(r'^sign_up/$', 'oj_user.views.sign_up', name='sign_up'),
    url(r'^logout/$', 'oj_user.views.sign_out', name='logout'),
    url(r'^sign_in/$', 'oj_user.views.sign_in', name='sign_in'),
    url(r'^check_in/$', 'oj_user.views.check_in', name='check_in'),
    url(r'^user_info/$', 'oj_user.views.user_info', name='user_info'),
    url(r'^get_code/$', 'oj_user.views.get_code', name='get_code'),

    url(r'^about/$', 'about.views.about', name="about"),

    url(r'^status_list/$', 'solution.views.solution_list', name='status_list'),
    url(r'^code/$', 'solution.views.code', name='code'),

    url(r'^re_error_detial/$', 'solution.views.re_error_detial', name='re_error_detial'),
    url(r'^ce_error_detial/$', 'solution.views.ce_error_detial', name='ce_error_detial'),
    url(r'^contest_list/$', 'contest.views.contest_list', name='contest_list'),
    url(r'^contest_problem_list/', 'contest.views.contest_problem_list', name='contest_problem_list'),
    url(r'^contest_status/', 'solution.views.contest_solution_list', name='contest_status'),
    url(r'^rank/$', 'oj_user.views.rank', name='rank'),
    url(r'^contest_rank/$', 'contest.views.contest_rank', name='contest_rank'),
    url(r'^contest_rank_xls/$', 'contest.views.contest_rank', name='contest_rank_xls')

)
