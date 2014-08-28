# -*- coding: utf-8 -*-  
from random import choice
import re
import time, datetime
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from DjangoVerifyCode import Code
from django.core.exceptions import ObjectDoesNotExist
from oj_user.models import User_oj, Privilege
from problem.models import Problem
from solution.models import Solution

from django.db.models import Sum, Q
from qduoj import config
from qduoj.config import *

from admin_oj.util import Authorization

@Authorization(ACCESS_BACKEND)
def index(request, *args, **kwargs):

    response_dict = kwargs.get('response_dict', {})

    user_oj = request.user.user_oj
 

    return render(request, 'admin_oj/index.html', response_dict)


def sign_in(request):
    if request.method == 'POST':
        next_url = request.POST.get('next', '/')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        captcha = request.POST.get('captcha', '')

        if not captcha:
            error = 'Verification code error !'
            return render(request, "user/sign_in.html",
                    {'error' : error, 'next' : next_url})
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
    
