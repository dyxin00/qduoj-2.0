# -*- coding: utf-8 -*-

import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from util import request_method_only
from problem.models import Problem
from solution.models import Solution, Custominput, Source_code
from contest.models import Contest
from oj_user.models import User_oj

from django.db.models import Q

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
    
        username = request.user.username
        solution = Solution.objects.filter(Q(**kwargs) | (Q(user__user__username=username) & Q(problem__visible=False)))

        return render(request, "solution/status.html", 
                {'judge_list' : solution,
                 'result_type' : result,
                 'language_type' : language})

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
