# -*- coding: utf-8 -*-  
from random import choice
import re
import time, datetime
import json
from  PIL import ImageFile

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect  
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from DjangoVerifyCode import Code
from django.core.exceptions import ObjectDoesNotExist
from oj_user.models import User_oj, Privilege

from qduoj import config
from qduoj.config import *

from admin_oj.util import Authorization


def log(request):
    user = request.user
    if user.is_anonymous():
        return render(request, 'admin_oj/login.html',{})
    return HttpResponseRedirect('/admin_oj/index')


@Authorization(ACCESS_BACKEND)
def index(request, *args, **kwargs):

    response_dict = kwargs.get('response_dict', {})
    user = request.user.user_oj
    response_dict['user'] = user
    return render(request, 'admin_oj/index.html', response_dict)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            return HttpResponse(json.dumps({'status': 203}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': 403}),content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': 403}),content_type="application/json")

def sign_out(request):
    logout(request)
    return render(request, 'admin_oj/login.html',{})
