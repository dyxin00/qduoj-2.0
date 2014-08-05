# -*- coding: utf-8 -*-

import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from util import request_method_only
from problem.models import Problem
from solution.models import Solution, Custominput, Source_code, Compileinfo, Runtimeinfo
from contest.models import Contest
from oj_user.models import User_oj

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

        solution = Solution.objects.filter(**kwargs)


        return render(request, "solution/status.html", 
                {'judge_list' : solution,
                 'result_type' : result,
                 'language_type' : language})

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
    
