# -*- coding: utf-8 -*-  
from random import choice
import re
import time, datetime
import json
import os
from  PIL import ImageFile

from django.shortcuts import render, redirect
from django.http import HttpResponse
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
from problem.models import Problem
from solution.models import Solution

from django.db.models import Sum, Q
from qduoj import config
from qduoj.config import *

from admin_oj.util import Authorization

@Authorization(ADD_PRO)
def get_problem_list(request, *args, **kwargs):

    response_dict = kwargs.get('response_dict', {})
    user = response_dict['user']
    page = int(request.GET.get('page', 0))
    classify = int(request.GET.get('classify', -1))

    index_start = page * PAGE_COUNT
    index_end = (page + 1) * PAGE_COUNT
    flag = 0
    check = {'visible' : True, 'user' : user}
    if classify != -1:
        check['classify'] = classify
    info = ('id', 'title', 'user__user__username', 'visible')

    if response_dict['privilege']  & PROBLEM_VISIBLE != 0:
        del check['user']

    if response_dict['privilege']  & ADD_CON_AND_PRO_AND_VIS != 0:
        del check['visible']

    problem = Problem.objects.filter(**check).values(*info)
    if classify != -1:
        problem_list = problem
    else:
        problem_list = problem[index_start : index_end]
    num = problem.count()
    if index_end > num:
        index_end = num
        flag = 1

    response_dict['problem_list'] = list(problem_list)
    del response_dict['user']
    response_dict['flag'] = flag
    return HttpResponse(json.dumps(response_dict), content_type="application/json")

@Authorization(ADD_PRO)
def problem_add(request, *args, **kwargs):

    key = {
        'title' : request.POST.get('title', None),
        'description' : request.POST.get('desc', None),
        'pro_input' : request.POST.get('desc_input', None),
        'pro_output' : request.POST.get('desc_output', None),
        'sample_input' : request.POST.get('sample_input', None),
        'sample_output' : request.POST.get('sample_output', None),
        'hint' : request.POST.get('hint', None),
        'source' : request.POST.get('source', None),
        'time_limit' : int(request.POST.get('timelimit', 0)),
        'memory_limit' : int(request.GET.get('memorylimit', 0)),
        'classify' : int(request.POST.get('classify', 0)),
        'user' : request.user.user_oj,
        'difficult' : int(request.POST.get('difficult',0)),
    }
    try:
        Problem.objects.create(**key)
        return HttpResponse(json.dumps({'status': 200}), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'status': 503}), content_type="application/json")

def problem_fix(request):
    pid = request.POST.get('id', None)
    if pid:
        problem = Problem.objects.get(id=pid)
        problem.title = request.POST.get('title', None)
        problem.description = request.POST.get('desc', None)
        problem.pro_input = request.POST.get('desc_input', None)
        problem.pro_output = request.POST.get('desc_output', None)
        problem.sample_input = request.POST.get('sample_input', None)
        problem.sample_output = request.POST.get('sample_output', None)
        problem.hint = request.POST.get('hint', None)
        problem.source = request.POST.get('source', None)
        problem.time_limit = int(request.POST.get('timelimit', 0))
        problem.memory_limit = int(request.GET.get('memorylimit', 0))
        problem.classify = int(request.POST.get('classify', 0))
        problem.user = request.user.user_oj
        problem.difficult = int(request.POST.get('difficult',0))
        problem.save()
        return HttpResponse(json.dumps({'status': 200}), content_type="application/json")

    else:
        return HttpResponse(json.dumps({'status': 504}), content_type="application/json")

@Authorization(ADD_PRO)
def problem_get(request, *args, **kwargs):
    pid = request.GET.get("id", 0)
    response_dict = kwargs.get('response_dict', {})
    try:
        problem = Problem.objects.get(id=pid)
        response_dict['problem'] = model_to_dict(problem)
        response_dict['status'] = 200
        del response_dict['user']
        response_dict['user'] = problem.user.user.username
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status': 400}), content_type="application/json")
    return HttpResponse(json.dumps(response_dict), content_type="application/json")

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def problem_visible(request, *args, **kwargs):
    pid = request.GET.get("id", 0) 
    problem = Problem.objects.get(id=pid)
    problem.visible = not problem.visible
    problem.save()
    return HttpResponse(json.dumps({'status' : '200'}), content_type="application/json")

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def problem_rejudge(request, *args, **kwargs):
    pid = request.GET.get('id', 0)
    try:
        problem = Problem.objects.get(id=pid)
        Solution.objects.filter(problem=problem).update(result=1)

    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status': 403}), content_type="application/json")

    return HttpResponse(json.dumps({'status': 200}), content_type="application/json")

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def solution_rejudge(request, *args, **kwargs):
    sid = request.GET.get('id', 0)
    try:
        solution = Solution.objects.get(id=sid)
        solution.result = 1
        solution.save()

    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status': 403}), content_type="application/json")
    
    return HttpResponse(json.dumps({'status': 200}), content_type="application/json")

@csrf_exempt
def image_upload(request):
    in_time = time.time()
    data = request.FILES.get('imgFile', None)
    if data == None:
        return HttpResponse(json.dumps({"error" : 1, "url" : ""}))

    parser = ImageFile.Parser()
    for chunk in data.chunks():
        parser.feed(chunk)
    image = parser.close()
    dir_img = os.path.dirname(__file__) + '/..'
    image.save(dir_img + "/static/problem_img/%s"%str(int(in_time))+ '-' + str(data))
    return HttpResponse(json.dumps({"error" : 0, "url" : "/static/problem_img/%s"%str(int(in_time)) + '-' + str(data)}))

