# -*- coding: utf-8 -*-  
from random import choice

from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from DjangoVerifyCode import Code

from oj_user.models import User_oj

import re   #francis

def index(request):
    return render(request, "index.html", {})

# The HttpResponse Used to test
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        school_id = request.POST.get('school_ID', '')
        password = request.POST.get('password', '')
        #未验证数据正确性, 合法性
        
        if not re.match(ur'[a-zA-Z0-9_\u4e00-\u9fa5]{2,20}$', unicode(username)):
            return render(request, "user/sign_up.html",
                    {"error": 'Username malformed'})

        if not re.match(ur'[0-9]{9,11}', unicode(school_id)):
            error = 'ID malformed'
            return render(request, "user/sign_up.html", {'error': error})

        if not re.match(ur'[\w!#$%&*+/=?^_`{|}~-]+(?:\.[\w!#$%&*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?', email):
            error = 'Email malformed'
            return render(request, "user/sign_up.html", {'error': error})

        if not re.match(ur'.{3,20}', password):
            error = 'Password malformed (can not be less than three)'
            return render(request, "user/sign_up.html", {'error': error})

        try:
            user = User.objects.create_user(username=username,
                             password=password, email=email)
        except IntegrityError:
            error = 'This user name already exists !'
            return render(request, "user/sign_up.html", {'error' : error})

        oj_user = User_oj.objects.create(user=user, school_id=school_id)
        return redirect('sign_in')
    return render(request, "user/sign_up.html", {})

# The HttpResponse Used to test
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        captcha = request.POST.get('captcha', '')

        if not captcha:
            return HttpResponse("captcha")
        code = Code(request)
        if not code.check(captcha):
            error = 'Verification code error !'
            return render(request, "user/sign_in.html", {'error' : error})

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.POST.get('next', '/'))
            else:
                error = 'The account has been stopped using !'
                return render(request, "user/sign_in.html", {'error' : error})
        else:
            error = 'The user name or password is incorrect !'
            return render(request, "user/sign_in.html", {'error' : error})
    next_url = request.GET.get('next', '/')
    return render(request, "user/sign_in.html", {'next' : next_url})


def sign_out(request):

    logout(request)
    return redirect('index')

@login_required(login_url='sign_in')
def user_info(request):

    return render(request, "user/user_info_page.html", {})

#http://www.oschina.net/p/django-verify-code/similar_projects?lang=26&sort=view
def get_code(request):

    code = Code(request)
    code.img_height = 46
    code.type = choice(['number', 'world'])
    return code.display()

