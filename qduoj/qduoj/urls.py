from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qduoj.views.home', name='home'),
    # url(r'^qduoj/', include('qduoj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^problem_index/$', 'problem.views.index', name='problem_index'),
    url(r'^problem/$', 'problem.views.problem', name='problem'),
    url(r'^sign_up/$', 'oj_user.views.sign_up', name='sign_up'),
    url(r'^sign_in/$', 'oj_user.views.sign_in', name='sign_in'),
)
