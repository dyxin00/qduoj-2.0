# -*- coding: utf-8 -*-  
from random import choice

from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from DjangoVerifyCode import Code

from oj_user.models import User_oj

# The HttpResponse Used to test
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        school_id = request.POST.get('school_ID', '')
        password = request.POST.get('password', '')
        #未验证数据正确性

        try:
            user = User.objects.create_user(username=username,
                             password=password, email=email)
        except IntegrityError:
            return HttpResponse("fail")

        oj_user = User_oj.objects.create(user=user, school_id=school_id)

        return HttpResponse("success")
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
            return HttpResponse("captcha wrong")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("success")
            else:
                return HttpResponse("not active")
        else:
            return HttpResponse("fail")
    return render(request, "user/sign_in.html", {})


def sign_out(request):

    logout(request)
    return HttpResponse("logout")

def user_info(request):
    return render(request, "user/user_info_page.html", {})
#http://www.oschina.net/p/django-verify-code/similar_projects?lang=26&sort=view
def get_code(request):

    code = Code(request)
    code.img_height = 46
    code.type = choice(['number', 'world'])
    return code.display()

