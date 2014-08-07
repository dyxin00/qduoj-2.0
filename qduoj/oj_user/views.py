# -*- coding: utf-8 -*-  
from random import choice
import re
import time, datetime

from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from DjangoVerifyCode import Code

from util import request_method_only
from oj_user.models import User_oj
from problem.models import Problem
from solution.models import Solution

from django.db.models import Sum

def index(request):
    return render(request, "index.html", {})

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        school_id = request.POST.get('school_ID', '')
        password = request.POST.get('password', '')
        
        if not re.match(ur'[a-zA-Z0-9_\u4e00-\u9fa5]{2,20}$', unicode(username)):
            return render(request, "user/sign_up.html",
                    {"error": 'Username is invalid or already taken'})

        if not re.match(ur'[0-9]{9,11}', unicode(school_id)):
            error = 'ID is invalid or already taken'
            return render(request, "user/sign_up.html", {'error': error})

        if not re.match(ur'[\w!#$%&*+/=?^_`{|}~-]+(?:\.[\w!#$%&*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?', email):
            error = 'Email is invalid'
            return render(request, "user/sign_up.html", {'error': error})

        if not re.match(ur'.{3,20}', password):
            error = 'Password is invalid(can not be less than three)'
            return render(request, "user/sign_up.html", {'error': error})

        try:
            user = User.objects.create_user(username=username,
                             password=password, email=email)
        except IntegrityError:
            error = 'This user name already exists !'
            return render(request, "user/sign_up.html", {'error' : error})
        
        oj_user = User_oj.objects.create(user=user, school_id=school_id)
        return render(request, 'delay_jump.html', {
            'next_url' : '/sign_in/',
            'info' : 'Registration successful'
            })

    return render(request, "user/sign_up.html", {})

def sign_in(request):
    if request.method == 'POST':
        next_url = request.POST.get('next', '/')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        captcha = request.POST.get('captcha', '')

        if not captcha:
            return HttpResponse("captcha")
        code = Code(request)
        if not code.check(captcha):
            error = 'Verification code error !'
            return render(request, "user/sign_in.html",
                    {'error' : error, 'next' : next_url})

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'delay_jump.html', {
                    'next_url' : next_url,
                    'info' : 'Login successful'
                    })
            else:
                error = 'The account has been stopped using !'
                return render(request, "user/sign_in.html",
                        {'error' : error, 'next' : next_url})
        else:
            error =''
            return render(request, "user/sign_in.html",
                    {'error' : error, 'next' : next_url})
    next_url = request.GET.get('next', '/')
    return render(request, "user/sign_in.html", {'next' : next_url})

def sign_out(request):
    logout(request)

    return render(request, 'delay_jump.html', {
        'next_url' : '/',
        'info' : 'Logout successful'
        })

def check_in(request):
    if request.method == 'POST':
        next_url = request.POST.get('next', '/')
        user_id = request.user.id
        user_oj = User_oj.objects.get(user__id = user_id)

        GMT_FORMAT = '%Y-%m-%d %H:%M:%S'
        now = time.localtime()
        accesstime = user_oj.accesstime
        if accesstime != None:
            t1 = user_oj.accesstime.replace() + datetime.timedelta(hours=8)
            st = time.mktime(time.strptime( str(t1),'%Y-%m-%d'))
            accesstime = time.localtime(st)
            if now[0] == accesstime[0] and now[1] == accesstime[1] and now[2] == accesstime[2]:
                return render(request, 'delay_jump.html',{
                    'next_url' : '/',
                    'info' : 'Dont recheck_in'
                    })
            else:
	        user_oj.integral = user_oj.integral + 1
                user_oj.accesstime = datetime.datetime.now()
                user_oj.save()
            
                return render(request, 'delay_jump.html', {
                    'next_url' : '/',
                    'info' : 'Check_in successful',
                    })
        else:
            user_oj.integral = user_oj.integral + 1
            user_oj.accesstime = datetime.datetime.now()
            user_oj.save()
            
            return render(request, 'delay_jump.html', {
                'next_url' : '/',
                'info' : 'Check_in successful',
                })



def user_info(request):
    if request.method=="GET":
        username = request.GET.get('username', '-1')
        if username != '-1':
            user_info = User.objects.get(username=username)
            user_id = user_info.id
        else:
            user_id = request.user.id
            user_info = request.user
        solution_list = Solution.objects.filter(user_id=user_id)
    
        accepted_list = solution_list.filter(result=4).order_by('problem').\
                values_list('problem', flat=True).distinct()
        unsolved_list = solution_list.exclude(result=4).order_by('problem').\
                values_list('problem', flat=True).distinct()
        unsolved_num = len(list(set(unsolved_list).difference(set(accepted_list))))
        '''
        count = 0
        for ac_id in accepted_list:
            problem = Problem.objects.get(id = ac_id)
            count = count + problem.difficult
        '''
        ac_problem = Problem.objects.filter(id__in = accepted_list)
        count = ac_problem.aggregate(Sum('difficult'))
        user_info.user_oj.integral = user_info.user_oj.integral + count['difficult__sum']
        accesstime_info = user_info.user_oj.accesstime
        if accesstime_info != None:
            accesstime = accesstime_info.replace() + datetime.timedelta(hours=8)
            flag = 0
        else:
            flag = 1
        user_infos = {'user_info': user_info, 
                'accepted_list': accepted_list,
                'unsolved_list': unsolved_list,
                'unsolved_num' : unsolved_num,
                'flag' : flag
                }
    return render(request, "user/user_info_page.html", user_infos)

#http://www.oschina.net/p/django-verify-code/similar_projects?lang=26&sort=view

@request_method_only('GET')
def get_code(request):

    code = Code(request)
    code.img_height = 46
    code.type = choice(['number', 'world'])
    return code.display()

def rank(request):
    if request.method == 'GET':
        page = request.GET.get('page', '1') 

        rank_list = User_oj.objects.all()
        
        user_list=rank_list.filter()
        #user_list=rank_list.filter().order_by('-solved', 'submit')
        return render(request, 'rank/rank.html', {'user_list' : user_list, 'page' : int(page)})
    
    error = "呵呵"
    return render(request, 'error.html', {'error' : error})
