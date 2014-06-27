# -*- coding: utf-8 -*-    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from problem.models import Problem
from solution.models import Solution, Custominput, Source_code
from django.core.exceptions import ObjectDoesNotExist
from contest.models import Contest
import re

def index(request):
    
    return render(request,"problem/problem_list.html", {})

def problem(request):
    if request.method == 'GET':
        pid = request.GET.get('pid', None)
        cid = request.GET.get('cid', None)
        if pid == None:
            error="Not Found !"
            return render(request, "error.html", {'error':error})
       
        if not re.match(ur'[0-9]+$', unicode(pid)):
            error="Only number please!"
            return render(request, "error.html", {'error':error})
        else:
            try:
                problem = Problem.objects.get(id=pid)
            except ObjectDoesNotExist:
                error="The problem not exist!"
                return render(request, "error.html", {'error':error})
            return render(request, "problem/problem.html",
                    {'problem' : problem, 'cid' : cid})
    else:
        error="~ ~呵呵！！"
        return render(request,"error.html", {'error':error})


@login_required(login_url='sign_in')
def submit_code(request):

    if request.method == 'POST':

        code = request.POST.get('code', None)
        language = request.POST.get('language', None)
        pid = request.POST.get('pid', None)
        cid = request.POST.get('cid', None)

        if len(code) == 0:
            error="Code too short!"
            return render(request, "error.html", {'error':error})

        try:
            submit = {
                    'user' : request.user.user_oj,
                    'problem' : Problem.objects.get(id=pid),
                    'ip' : request.META.get('REMOTE_ADDR'),
                     'code_length' : len(code)
                     }
        except ObjectDoesNotExist:
            error="The problem not exist!"
            return render(request, "error.html", {'error':error})

        if cid != None:
            try:
                cid = Contest.objects.get(id=cid)
                submit['cid'] = cid
            except ObjectDoesNotExist:
                error='The contest not exist!'
                return render(request, "error.html", {'error':error})
        
        solution = Solution.objects.create(**submit)
        Source_code.objects.create(solution=solution, source=code)

        return render(request, 'delay_jump.html', {'next_url' : '/status_list/'})
        #return redirect('status_list')

    error="~ ~呵呵！！"
    return render(request,"error.html", {'error':error})
