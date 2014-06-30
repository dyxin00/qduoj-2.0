# -*- coding: utf-8 -*-  
from random import choice
import re

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

@login_required(login_url='sign_in')
def user_info(request):
    if request.method=="GET":

        user_id = request.user.id
        solution_list = Solution.objects.filter(user_id=user_id)
    
        accepted_list = solution_list.filter(result=4).order_by('problem').values_list('problem', flat=True).distinct()
        unsolved_list = solution_list.exclude(result=4).order_by('problem').values_list('problem', flat=True).distinct()
        unsolved_num = len(list(set(unsolved_list).difference(set(accepted_list))))
    return render(request, "user/user_info_page.html", {'accepted_list': accepted_list, 'unsolved_list': unsolved_list, 'unsolved_num' :unsolved_num})

#http://www.oschina.net/p/django-verify-code/similar_projects?lang=26&sort=view

@request_method_only('GET')
def get_code(request):

    code = Code(request)
    code.img_height = 46
    code.type = choice(['number', 'world'])
    return code.display()

