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
from django.forms.models import model_to_dict
from DjangoVerifyCode import Code
from django.core.exceptions import ObjectDoesNotExist
from oj_user.models import User_oj, Privilege
from problem.models import Problem
from contest.models import Contest, Contest_problem, ContestPrivilege
from solution.models import Sim, Solution, Source_code

from django.db.models import Sum, Q
from qduoj import config
from qduoj.config import *

from admin_oj.util import Authorization

@Authorization(ADD_PRO)
def get_contest_list(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    user = response_dict['user']
    page = int(request.GET.get('page', 0))

    index_start = page * PAGE_COUNT
    index_end = (page + 1) * PAGE_COUNT
    flag = 0
    check = {'visible' : True, 'user' : user}
    info = ('id', 'title', 'user__user__username', 'visible')

    if response_dict['privilege']  & PROBLEM_VISIBLE != 0:
        del check['user']

    if response_dict['privilege']  & ADD_CON_AND_PRO_AND_VIS != 0:
        del check['visible']

    contest = Contest.objects.filter(**check).values(*info)
    if page != 0:
        contest_list = contest[index_start : index_end]
    else:
        contest_list = contest
    num = contest.count()
    if index_end > num:
        index_end = num
        flag = 1

    response_dict['contest_list'] = list(contest_list)
    del response_dict['user']
    response_dict['flag'] = flag
    return HttpResponse(json.dumps(response_dict), content_type="application/json")

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def contest_add(request, *args, **kwargs):
    arry = request.GET.get('problems', None)
    problem_info = json.loads(arry)
    
    problem_list = []
    for problem in problem_info:
        problem_list.append(problem['p_id'])

    start_time = request.GET.get('start_data') + ' ' + request.GET.get('start_day')
    end_time = request.GET.get('end_data') + ' ' + request.GET.get('end_day')
    open_rank = False
    if request.GET.get('contest_openrank') == 'true':
        open_rank = True
    key = {
        'title' : request.GET.get('title', None),
        'start_time': start_time,
        'end_time' : end_time,
        'user' : request.user.user_oj,
        'description' : request.GET.get('desc', None),
        'private' : int(request.GET.get('contest_classify', 0)),
        'open_rank' : open_rank,
        'langmask' : int(request.GET.get('contest_langmask', 0)),
        'mode' : int(request.GET.get('contest_mode', None)),
    }
    problems = Problem.objects.filter(id__in=problem_list)
    
    try:
        contest = Contest.objects.create(**key)
        count = 0
        for problem in problems:
            key_problem = {
                'problem' : problem,
                'contest' : contest,
                'title' : problem_info[count]['title'],
                'num' : int(problem_info[count]['num']),
                'sorce' : int(problem_info[count]['score']),
            }
            try:
                count = count + 1
                Contest_problem.objects.create(**key_problem)
            except:
                return HttpResponse(json.dumps({'status': 401}), content_type="application/json")

        if contest.private == 1:
            contest_user_list = request.GET.get('privilege_user', None)
            contest_user = contest_user_list.split(',')
            user_list = User_oj.objects.filter(user__username__in=contest_user)
            for user in user_list:
                key_user = {
                    'user': user,
                    'contest': contest,
                }
                try:
                    ContestPrivilege.objects.create(**key_user)
                except:
                    return HttpResponse(json.dumps({'status': 402}), content_type="application/json")
        else:
            pass
        return HttpResponse(json.dumps({'status': 200}), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'status': 403}), content_type="application/json")

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def contest_get(request, *args, **kwargs):
    cid = request.GET.get('id', 0)
    response_dict = kwargs.get('response_dict', {})
    try:
        contest = {}
        contest_obj = Contest.objects.get(id=cid)
        contest = model_to_dict(contest_obj)
        del contest['start_time'], contest['end_time']
        response_dict['contest'] = contest
        response_dict['status'] = 200
        del response_dict['user']
        response_dict['user'] = contest_obj.user.user.username
        info = (
            'problem__id',
            'problem__title',
            'problem__user__user__username',
            'num',
            'sorce',
            'title',
        )
        problems = Contest_problem.objects.select_related(depth=3).filter(contest=contest_obj).values(*info)
        user = (
            'user__user__username',
        )
        users = ContestPrivilege.objects.select_related(depth=3).filter(contest=contest_obj).values(*user)
        response_dict['problems'] = list(problems)
        response_dict['users'] = list(users)
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status': 403}), content_type="application/json")

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def contest_fix(request, *args, **kwargs):
    cid = request.GET.get('id', 0)
    contest = Contest.objects.get(id=cid)

    start_time = request.GET.get('start_data') + ' ' + request.GET.get('start_day')
    end_time = request.GET.get('end_data') + ' ' + request.GET.get('end_day')
    	
    open_rank = False
    if request.GET.get('contest_openrank') == 'true':
        open_rank = True

    contest.title = request.GET.get('title', None)
    contest.start_time = start_time
    contest.end_time = end_time
    contest.user = request.user.user_oj
    contest.description = request.GET.get('desc', None)
    contest.private = int(request.GET.get('contest_classify', 0))
    contest.open_rank = open_rank
    contest.langmask = int(request.GET.get('contest_langmask', 0))
    contest.mode = int(request.GET.get('contest_mode', 0))
    contest.save()
    print request.GET.get('contest_classify')    
    arry = request.GET.get('problems', None)
    problem_info = json.loads(arry)
    contest_problem = Contest_problem.objects.select_related(depth=3).filter(contest=contest)
    contest_problem.delete()
    problem_list = []
    for problem in problem_info:
        problem_list.append(problem['p_id'])

    problems = Problem.objects.select_related(depth=3).filter(id__in=problem_list)
    count = 0
    for problem in problems:
        key_problem = {
            'problem' : problem,
            'contest' : contest,
            'title' : problem_info[count]['title'],
            'num' : int(problem_info[count]['num']),
            'sorce' : int(problem_info[count]['score']),
        }
        try:
            count = count + 1
            Contest_problem.objects.create(**key_problem)
        except:
            return HttpResponse(json.dumps({'status':401}), content_type="application/json")


    contest_user = ContestPrivilege.objects.select_related(depth=3).filter(contest=contest)
    contest_user.delete()
    if contest.private == 1:
        contest_user_list = request.GET.get('privilege_user', None)
        contest_user = contest_user_list.split(',')
        user_list = User_oj.objects.filter(user__username__in=contest_user)
        for user in user_list:
            key_user = {
                'user': user,
                'contest': contest,
            }
            try:
                ContestPrivilege.objects.create(**key_user)
            except:
                return HttpResponse(json.dumps({'status':402}),content_type="application/json")

    return HttpResponse(json.dumps({'status':200}),content_type="application/json")

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def get_contest_sim(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    cid = request.GET.get('id', 0)
    if response_dict['privilege'] & ADD_CON_AND_PRO_AND_VIS != 0:
        solutions = Solution.objects.select_related(depth=3).filter(contest__id=cid)
        value = {
            'solution__id',
            'sim_s_id',
            'sim',
            'solution__user__user__username',
            'solution__contest__title',
        }
        sim = Sim.objects.select_related(depth=3).filter(solution__in=solutions).values(*value)
                #filter(Q(solution__in=solutions) & Q(sim_s_id__user__user__username__ne=solution__user__user__username)).values(*value)
        del response_dict['user']
        response_dict['sim'] = list(sim)
    return HttpResponse(json.dumps(response_dict), content_type="application/json")

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def get_sim_code(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    sid = request.GET.get('sid', '0')
    smid = request.GET.get('smid', 0)
    sid_code = Source_code.objects.get(solution__id=sid)
    smid_code = Source_code.objects.get(solution__id=smid)
    
    solution_s = Solution.objects.get(id=sid)
    response_dict['sid_code'] = sid_code
    response_dict['solution_s'] = solution_s

    solution_sm = Solution.objects.get(id=smid)
    response_dict['smid_code'] = smid_code
    response_dict['solution_sm'] = solution_sm
    return render(request, 'admin_oj/get_sim_code.html', response_dict)


@Authorization(ADD_CON_AND_PRO_AND_VIS)
def contest_visible(request, *args, **kwargs):
    cid = request.GET.get("id", 0)
    contest = Contest.objects.get(id=cid)
    contest.visible = not contest.visible
    contest.save()
    return HttpResponse(json.dumps({'status': 200}), content_type="application/json")
