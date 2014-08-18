from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from problem.models import Problem
from contest.models import Contest, Contest_problem, ContestPrivilege
from oj_user.models import User_oj
from solution.models import Solution

def contest_list(request):
    contests = Contest.objects.filter(visible=False)
    return render(request, 'contest/contest_list.html', {'contests': contests})

def contest_rank(request):
    if request.method=='GET':
        cid = request.GET.get('cid', None)
        page = request.GET.get('page', '1')

        if cid == None:
            error = "The contest is not exist!"
            return render(request, 'error.html', {'error': error})
         
        try:
            contest = Contest.objects.get(id=cid)
        except ObjectDoesNotExist:
            error = "The contest is not exist!"
            return render(request, 'error.html', {'error':error})

        #---------get contest_user_list----------------
        contest_user_id_list = Solution.objects.filter(contest__id=cid).\
                order_by('user__user__id').values_list('user__user__id', flat=True).distinct()
        contest_user_list = User_oj.objects.filter(user__id__in=contest_user_id_list)
        #print user_list
        
        contest_problem_list = Contest_problem.objects.filter(contest__id=cid)
        
        contest_info = []
        for contest_user in contest_user_list:
            
            grade = 0.0   
            accepted = 0       
            contest_user_loop = []
            contest_user_loop.append(contest_user.user.username)
            problem_info = []
            
            for problem in contest_problem_list:
                
                problem_loop = {}
                problem_loop['id'] = problem.problem.id
                
                try:
                    last_solution = Solution.objects.filter(contest__id=cid,\
                                problem__id=problem.problem.id, user__user__id=contest_user.user.id).order_by('-id')[0]
                    problem_score = float(last_solution.pass_rate) * problem.sorce
                    if problem_score == problem.sorce:
                        accepted += 1
                        problem_loop['AC'] = True
                    else:
                        problem_loop['AC'] = False
                    problem_loop['score'] = problem_score
                    problem_loop['submit'] = Solution.objects.filter(contest__id=cid,\
                                                problem__id=problem.problem.id,user__user__id=contest_user.user.id).count()
                    grade += problem_score

                except IndexError:
                    problem_loop['submit'] = -1
                    grade += 0
                problem_info.append(problem_loop)
                
            contest_user_loop.append(grade)
            contest_user_loop.append(accepted)
            contest_user_loop.append(Solution.objects.filter(contest__id=cid,\
                                                        user__user__id=contest_user.user.id).count())
            contest_user_loop.append(problem_info)

            contest_info.append(contest_user_loop)
        contest_info.sort(key=lambda t: (t[1], t[2], -t[3]), reverse=True)
        return render(request, 'rank/rank.html', {'user_list': contest_info,
                                                  'mode': contest.mode,
                                                  'page': int(page)})
