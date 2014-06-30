# -*- coding: utf-8 -*-

import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from problem.models import Problem
from solution.models import Solution, Custominput, Source_code
from contest.models import Contest
from oj_user.models import User_oj

def solution_list(request):
    #solution = Solution.objects.all();
    if request.method == 'GET':
        problem_id = request.GET.get('problem_id', None)
        user_name = request.GET.get('user_name', '')
        result = request.GET.get('result', '-1')
        language = request.GET.get('language', '-1')
        
        kwargs = { }

        if re.match(ur'[0-9]+$', unicode(problem_id)):
            kwargs['problem'] = problem_id

        if user_name != '':
            print ' 1' + user_name +'1 '
            kwargs['user__user__username'] = user_name

        if result != '-1':
            kwargs['result'] = result

        if language != '-1':
            kwargs['language'] = language
        solution = Solution.objects.filter(**kwargs)

        return render(request, "solution/status.html", 
                {'solution' : solution,
                 'result_type' : result,
                 'language_type' : language})
    error = "呵呵"
    return render(request, "error.html", {'error' : error})


