# -*- coding: utf-8 -*-

import re
import time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from util import request_method_only
from problem.models import Problem, Score
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
        kwargs['contest__id'] = None
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
                        'cid':cid})

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
        problem_id = request.GET.get('problem_id', None)

        kwargs = {}

        username = request.user.username

        if re.match(ur'[0-9]+$', unicode(problem_id)):
            kwargs['problem_id'] = problem_id    #待改正!!!

        kwargs['user__user__username']=username
        kwargs['contest_id']=cid

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

        #判断是否存在对应比赛
        if problem_id != None:
            try:
                Contest_problem(problem_id=problem_id, contest_id=cid)
            except:
                error = "The contest does not exist!"
                return render(request, "error.html", {'error':error})

       
        #出题者权限 
        contest_user = False
        if username == contest_obj.user.user.username:
            contest_user = True
        
        #未允许参加考试的不可见
        visit_contest = True
        try:
           ContestPrivilege.objects.get(user__user__username=username, contest_id=cid)
        except:
            visit_contest = False 
        if (visit_contest == False) and (ADMIN == False) and (contest_user == False) and (contest_obj.private == 1):
            error = "You do not have permission to view the results details!"
            return render(request, "error.html", {'error':error})

        #允许参加考试的未到时间的不可见
        now_time = contest_obj.start_or_not()
        if (ADMIN == False) and (contest_user == False) and now_time == False:
            error = "You do not have permission to view the results details!"
            return render(request, "error.html", {'error':error})
        
        #只有mode=1的只能看自己的
        if ADMIN == False and contest_user == False and contest_obj.mode == 1:
            solution_list = Solution.objects.select_related(depth=2).filter(**kwargs)
        else:
            del kwargs['user__user__username']
            solution_list = Solution.objects.select_related(depth=2).filter(**kwargs)
       
        solution_result_info = []
        for solution in solution_list:
            grade = 0.0
            solution_grade_loop = []
            solution_grade_loop.append(solution.id) #0
            try:
                problem_detial = Contest_problem.objects.get(problem_id=solution.problem_id, contest_id=cid)
                if solution.pass_rate == None:
                    grade = 0.0
                else:
                    grade = float(solution.pass_rate) * problem_detial.sorce
            except ObjectDoesNotExist:
                pass
            
            solution_grade_loop.append(grade) #1
            solution_grade_loop.append(solution) #2
            solution_result_info.append(solution_grade_loop)

        return render(request, "contest/contest_status.html", 
                      {'judge_list':solution_list, 'ADMIN':ADMIN, 
                       'contest_user':contest_user,
                       'mode':contest_obj.mode,
                       'solution_result_info':solution_result_info,
                       'cid': cid})



