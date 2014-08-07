# -*- coding: utf-8 -*-    
import re

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from util import request_method_only
from problem.models import Problem
from solution.models import Solution, Custominput, Source_code
from contest.models import Contest
from oj_user.models import User_oj, Privilege
from qduoj import config

@request_method_only('GET')
def index(request):
    if request.method == 'GET':

        problem_type = request.GET.get('type', '-1')

        username= request.user.username
        try:
            user_authority = Privilege.objects.get(user__user__username=username).authority
            if user_authority == config.ADMIN:
                problems = Problem.objects.all()
            else:
                problems = Problem.objects.filter(Q(visible=True) | (Q(user__user__username=username) & Q(visible=False)))
        except ObjectDoesNotExist:
            problems = Problem.objects.filter(Q(visible=True) | (Q(user__user__username=username) & Q(visible=False)))
            #error = "limited permissioin"
            #return render(request, "error.html", {'error':error})
 
        if problem_type != '-1':
            problems = problems.filter(classify=problem_type)

        problem_dict = {'problems': problems, 'type' : problem_type}
        if request.user.is_authenticated():
            solution_list = Solution.objects.filter(user_id=request.user.id)
            accepted = solution_list.filter(result=4).order_by('problem').\
                    values_list('problem', flat=True).distinct()
            unsolved = solution_list.exclude(result=4).order_by('problem').\
                    values_list('problem', flat=True).distinct()
            problem_dict['accepteds'] = accepted
            problem_dict['unsolveds'] = unsolved

        return render(request, "problem/problem_list.html", problem_dict)

@request_method_only('GET')
def problem(request):
    if request.method == 'GET':
        pid = request.GET.get('pid', None)
        cid = request.GET.get('cid', None)
        if pid == None:
            error = "Not Found !"
            return render(request, "error.html", {'error':error})
       
        if not re.match(ur'[0-9]+$', unicode(pid)):
            error = "Only number please!"
            return render(request, "error.html", {'error':error})
        else:
            try:
                problem = Problem.objects.get(id=pid)
            except ObjectDoesNotExist:
                error = "The problem not exist!"
                return render(request, "error.html", {'error':error})
            if problem.visible is True:
                return render(request, "problem/problem.html",
                        {'problem' : problem, 'cid' : cid})
            else:
                error = "The problem not exist!"
                return render(request, "error.html", {'error':error})


@login_required(login_url='sign_in')
@request_method_only('POST')
def submit_code(request):

    if request.method == 'POST':

        code = request.POST.get('code', None)
        language = request.POST.get('language', None)
        pid = request.POST.get('pid', None)
        cid = request.POST.get('cid', None)
        
        try:
            problem = Problem.objects.get(id=pid)
        except ObjectDoesNotExist:
            error = "The problem not exist!"
            return render(request, "error.html", {'error':error})

        if problem.visible == False:
            error = "The problem is invisible!"
            return render(request, "error.html", {'error':error})

        if len(code) == 0:
            error = "Code too short!"
            return render(request, "error.html", {'error':error})

        submit = {
                'user' : request.user.user_oj,
                'problem' : problem,
                'ip' : request.META.get('REMOTE_ADDR'),
                'code_length' : len(code),
                'language' : language
                }

        if cid != None:
            try:
                contest = Contest.objects.get(id=cid)
                submit['cid'] = contest
            except ObjectDoesNotExist:
                error = 'The contest not exist!'
                return render(request, "error.html", {'error':error})
        
        solution = Solution.objects.create(**submit)
        Source_code.objects.create(solution=solution, source=code)

        return render(request, 'delay_jump.html', {
            'next_url' : '/status_list/',
            'info' : 'Submitted successfully'
            })
