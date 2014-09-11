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
from contest.models import Contest_problem, ContestPrivilege
from qduoj import config


def index(request):
    if request.method == 'GET':

        problem_type = request.GET.get('type', '-1')
        problem_title = request.GET.get('problem_title', '')
        pid = request.GET.get('pid', None)

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
 
        kwargs = {}
        if problem_type != '-1':
            kwargs['classify'] = problem_type
        if re.match(ur'[0-9]+$', unicode(pid)):
            kwargs['id'] = pid

        problems = problems.filter(Q(**kwargs) & Q(title__icontains = problem_title))


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
        username = request.user.username
        if pid == None:
            error = "Not Found !"
            return render(request, "error.html", {'error':error})

        if not re.match(ur'[0-9]+$', unicode(pid)):
            error = "Only number please!"
            return render(request, "error.html", {'error':error})

        try:
            authority = Privilege.objects.get(user__user__username=username).authority
        except ObjectDoesNotExist:
            authority = None
        if cid == None:
            try:
                problem = Problem.objects.get(id=pid)
            except ObjectDoesNotExist:
                error = "The problem not exist!"
                return render(request, "error.html", {'error': error})
            if authority == config.ADMIN or problem.visible is True or problem.user.user.username == username:
				return render(request, "problem/problem.html", {'problem' : problem})
            else:
                error = "The problem not exist!"
                return render(request, "error.html", {'error':error})

        try:
            problem = Problem.objects.get(id=pid)
        except ObjectDoesNotExist:
            error = "The problem not exist!"
            return render(request, "error.html", {'error':error})
        if cid != None:
            try:
                Contest_problem.objects.get(contest__id = cid, problem__id = pid)
            except ObjectDoesNotExist:
                error = "The problem does not exist or belong to this contest!"
                return render(request, "error.html", {'error':error})

            try:
                contest = Contest.objects.get(id=cid)
            except ObjectDoesNotExist:
                error = "The contest does not exist!"
                return render(request, "error.html", {'error':error})

            if authority == config.ADMIN or problem.visible is True or (problem.user.user.username==username and problem.visible==False):
                return render(request, "problem/problem.html",
                            {'problem' : problem, 'cid': cid})
            if contest.start_or_not():
                if contest.private == 0: 
                    return render(request, "problem/problem.html",
                              {'problem' : problem, 'cid': cid})

                try:
                    ContestPrivilege.objects.get(contest__id = cid, user__user__username = username)
                    return render(request, "problem/problem.html",
                              {'problem' : problem, 'cid': cid})
                except ObjectDoesNotExist:
                    error = "Sorry, you are not permitted to attend the contest!"
                    return render(request, "error.html", {'error':error})

            error = "Sorry, the contest does not begin!"
            return render(request, "error.html", {'error':error})
        else:
            return render(request, "problem/problem.html",
                          {'problem': problem})


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
        
        username = request.user.username
        try:
            authority = Privilege.objects.get(user__user__username=username).authority
        except ObjectDoesNotExist:
            authority = None

        if cid == None:
            if problem.visible == False and authority != config.ADMIN and problem.user.user.username != username:
                error = "The problem is invisible!"
                return render(request, "error.html", {'error':error})
                
        else:
            try:
                contest = Contest.objects.get(id=cid)
            except ObjectDoesNotExist:
                error = "The contest does not exist!"
                return render(request, "error.html", {'error':error})

            if contest.start_or_not() != True or contest.end_or_not() != True:
                if not(authority == config.ADMIN or contest.user.user.username == username):
                    error = "The contest does begin or has ended!"
                    return render(request, "error.html", {'error':error})
            else:
                if contest.private:
                    try:
                        ContestPrivilege.objects.get(contest__id = cid, user__user__username = username)
                    except ObjectDoesNotExist:
                        if not(authority == config.ADMIN or contest.user.user.username == username):
                            error = "Sorry, you are not permitted to submit code!"
                            return render(request, "error.html", {'error':error})

        if len(code) == 0:
            error = "Code too short!"
            return render(request, "error.html", {'error':error})
        if cid != None:
            problem_obj = Contest_problem.objects.get(contest__id = cid, problem = problem)  
            submit = {
                    'user' : request.user.user_oj,
                    'problem' : problem,
                    'ip' : request.META.get('REMOTE_ADDR'),
                    'code_length' : len(code),
                    'language' : language,
                    'num' : problem_obj.num
                }
        else:
            submit = {
                    'user' : request.user.user_oj,
                    'problem' : problem,
                    'ip' : request.META.get('REMOTE_ADDR'),
                    'code_length' : len(code),
                    'language' : language,
                }


        if cid != None:
            try:
                contest = Contest.objects.get(id=cid)
                submit['contest'] = contest

            except ObjectDoesNotExist:
                error = 'The contest not exist!'
                return render(request, "error.html", {'error':error})
        
        solution = Solution.objects.create(**submit)
        Source_code.objects.create(solution=solution, source=code)
        if cid == None:
            return render(request, 'delay_jump.html', {
                'next_url' : '/status_list/',
                'info' : 'Submitted successfully'
                })
        else:
            return render(request, 'delay_jump.html', {
                'next_url' : '/contest_status/?cid=' + cid,
                'info' : 'Submitted successfully'
                })
