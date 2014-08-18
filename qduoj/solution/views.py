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
from contest.models import Contest, ContestPrivilege, Contest_problem
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
        #kwargs['problem__visible'] = True
    
        ADMIN = False
        username = request.user.username
        try:
            user_authority = Privilege.objects.get(user__user__username=username).authority
            if user_authority == config.ADMIN:
                ADMIN = True
               # del  kwargs['problem__visible']
                solution = Solution.objects.select_related(depth=2).filter(**kwargs)
                
            else:
                solution = Solution.objects.select_related(depth=2).filter(Q(**kwargs) \
                                            & (Q(problem__user__user__username=username) | Q(problem__visible=True)))
        except:
           # del kwargs['problem__visible']
            solution = Solution.objects.select_related(depth=2).filter(Q(**kwargs) \
                                            & (Q(problem__user__user__username=username) | Q(problem__visible=True)))
        
        return render(request, "solution/status.html", 
                {'judge_list' : solution,
                 'result_type' : result,
                 'language_type' : language,
                 'ADMIN' : ADMIN})

def code(request):
    if request.method == "GET":
        run_id = request.GET.get('runid', '')
        cid = request.GET.get('cid', 0)
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
                       'result' : result,
                       'cid' : cid})
'''
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

'''

def ce_error_detial(request):
    if request.method == 'GET':
        runid = request.GET.get('runid', -1)

        username = request.user.username
        ADMIN = False
        try:
            user_authority = Privilege.objects.get(user__user__username=username).authority
            if user_authority == config.ADMIN:
                ADMIN = True
        except:
            pass
        
        try:
            error_obj = Compileinfo.objects.get(solution_id = runid)
        except ObjectDoesNotExist:
            error = "This error does not exist!"
            return render(request, "error.html", {'error':error})

        if (ADMIN == True) or (username == error_obj.solution.user.user.username):
            return render(request, 'result_detial/result_detial.html', 
                      {'solution_info' : error_obj.solution, 'error_info':error_obj.error})
        
        error = "You do not have permission to view the results details!"
        return render(request, "error.html", {'error':error})
        

def re_error_detial(request):
    if request.method == 'GET':
        runid = request.GET.get('runid', '-1')

        username = request.user.username
        ADMIN = False
        try:
            user_authority = Privilege.objects.get(user__user__username=username).authority
            if user_authority == config.ADMIN:
                ADMIN = True
        except:
            pass

        try:
            error_obj = Solution.objects.get(id=runid)
        except ObjectDoesNotExist:
            error = "This error does not exist!"
            return render(request, "error.html", {'error':error})

        if (ADMIN == True) or (username == error_obj.user.user.username):
            return render(request, "result_detial/result_detial.html",
                      {'solution_info':error_obj})

        error = "You do not have permission to view the results details!"
        return  render(request, "error.html", {'error':error})

def contest_solution_list(request):
    if request.method == 'GET':
        cid = request.GET.get('cid', '-1')
        username = request.user.username
        ADMIN = False
        try:
            user_authority = Privilege.objects.get(user__user__username=username).authority
            if user_authority == config.ADMIN:
                ADMIN = True
        except:
            pass

        try:
            contest_obj = Contest.objects.get(id=cid)
        except:
            error = "The contest does not exist!"
            return render(request, "error.html", {'error':error})
        '''
        if contest_obj.mode == 0 and contest_obj.defunct == True:
            error = "结果 ? ? ?想吧 ! ! !"
            return render(request, "error.html", {'error':error})
        ''' 
        contest_user = False
        if username == contest_obj.user.user.username:
            contest_user = True
        
        visit_contest = True
        try:
           ContestPrivilege.objects.get(user__user__username=username, contest_id=cid)
        except:
            visit_contest = False 
        if (visit_contest == False) and (ADMIN == False) and (contest_user == False) and (contest_obj.private == 1):
            error = "You do not have permission to view the results details!"
            return render(request, "error.html", {'error':error})

        now_time = contest_obj.start_or_not()
        if (ADMIN == False) and (contest_user == False) and now_time == False:
            error = "You do not have permission to view the results details!"
            return render(request, "error.html", {'error':error})
        
        if ADMIN == False and contest_user == False and contest_obj.mode == 1:
            solution = Solution.objects.select_related(depth=2).filter(contest_id=cid, user__user__username=username)
            
        else:
            solution = Solution.objects.select_related(depth=2).filter(contest_id=cid)
        
        return render(request, "contest/contest_status.html", 
                      {'judge_list':solution, 'ADMIN':ADMIN, 
                       'contest_user':contest_user,
                       'mode':contest_obj.mode,
                       'cid': cid})
    
