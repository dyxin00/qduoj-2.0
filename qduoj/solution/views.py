# -*- coding: utf-8 -*-

import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from util import request_method_only
from problem.models import Problem
from solution.models import Solution, Custominput, Source_code, Compileinfo, Runtimeinfo
from contest.models import Contest
from oj_user.models import User_oj, Privilege
from qduoj import config

@request_method_only('GET')
def solution_list(request):
    if request.method == 'GET':
        problem_id = request.GET.get('problem_id', None)
        user_name = request.GET.get('user_name', '')
        result = request.GET.get('result', '-1')
        language = request.GET.get('language', '-1')
        
        kwargs = {}

        if re.match(ur'[0-9]+$', unicode(problem_id)):
            kwargs['problem'] = problem_id

        if user_name != '':
            kwargs['user__user__username'] = user_name

        if result != '-1':
            kwargs['result'] = result

        if language != '-1':
            kwargs['language'] = language
        kwargs['problem__visible'] = True
    
        ADMIN = False
        username = request.user.username
        try:
            user_authority = Privilege.objects.get(user__user__username=username).authority
            if user_authority == config.ADMIN:
                ADMIN = True
                solution = Solution.objects.select_related(depth=2).all()
            else:
                solution = Solution.objects.select_related(depth=2).filter(Q(**kwargs) | (Q(user__user__username=username) & Q(problem__visible=False)))
        except:
            solution = Solution.objects.select_related(depth=2).filter(Q(**kwargs) | (Q(user__user__username=username) & Q(problem__visible=False)))
        
        return render(request, "solution/status.html", 
                {'judge_list' : solution,
                 'result_type' : result,
                 'language_type' : language,
                 'ADMIN' : ADMIN})

def code(request):
    if request.method == "GET":
        run_id = request.GET.get('runid', '')
        try:
            solution = Solution.objects.get(id=run_id)
        except ObjectDoesNotExist:
            error = "The solution not exist!"
            return render(request, "error.html", {'error':error})

        try:
            source_code = Source_code.objects.get(solution=solution)
        except ObjectDoesNotExist:
            error = "The code not exist!"
            return render(request, "error.html", {'error':error})

        answer = ['Pending'] * 4 + ['Accepted', 'Presentation Error',
                                'Wrong Answer', 'Time Limit',
                                'Memory Limit', 'Output Limit',
                                'Runtime Error', 'Compile Error'
                                ]
        result = answer[solution.result]
        return render(request, "solution/code.html",
                      {'solution' : solution,
                       'source_code' : source_code,
                       'result' : result})

def result_detial(request):
    if request.method == 'GET':
        runid = request.GET.get('runid', -1)

        username = request.user.username

        try:
            ce_obj = Compileinfo.objects.get(solution_id = runid, solution__user__user__username = username)
        except ObjectDoesNotExist:
            try:
                re_obj = Solution.objects.get(id = runid, user__user__username = username)
            except ObjectDoesNotExist:
                error = "You do not have permission to view the results details!"
                return render(request, "error.html", {'error':error})

            return render(request, 'result_detial/result_detial.html', 
                    {'solution_info' : re_obj})
        
        return render(request, 'result_detial/result_detial.html', 
                {'solution_info' : ce_obj.solution, 'error_info' : ce_obj.error})
    
