from django.shortcuts import render, redirect
from problem.models import Problem, Score
from contest.models import Contest, Contest_problem, ContestPrivilege
from solution.models import Solution, Custominput, Source_code
from oj_user.models import User_oj, Privilege
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
import time, datetime
from qduoj import config

def contest_list(request):
    if request.method == 'GET':
        status = request.GET.get('status', -1)
        username = request.user.username
        try:
            user_authority = Privilege.objects.get(user__user__username = username).authority
            if user_authority == config.ADMIN:
                contests = Contest.objects.all()
            else:
                contests = Contest.objects.select_related(depth=3).filter(Q(visible=True) | (Q(user__user__username = username) & Q(visible=False)))

        except ObjectDoesNotExist:
            contests = Contest.objects.select_related(depth=3).filter(Q(visible=True) | (Q(user__user__username = username) & Q(visible=False)))
        for contest in contests:
            if (contest.start_or_not() <= True and contest.end_or_not() == True) or (contest.start_or_not() == False):
                if contest.defunct:
                    contest.defunct = False
                    contest.save()
            else:
                if contest.defunct == False:
                    contest.defunct = True
                    contest.save()
        if status == '1':
            contests = contests.select_related(depth=3).filter(defunct = False)
        else:
            contests = contests.select_related(depth=3).filter(defunct = True)
        return render(request, 'contest/contest_list.html', {'contests': contests})

def contest_problem_list(request):
    if request.method == 'GET':
        cid = request.GET.get('cid', None)
        if cid != None:
            try:
                contest = Contest.objects.get(id = cid)
                now = time.time()
                t1 = contest.start_time.replace(tzinfo=None) + datetime.timedelta(hours=8)
                t2 = contest.end_time.replace(tzinfo=None) + datetime.timedelta(hours=8)
                start_time = float(time.mktime(time.strptime( str(t1),'%Y-%m-%d %H:%M:%S'))) - now
                end_time = float(time.mktime(time.strptime( str(t2),'%Y-%m-%d %H:%M:%S'))) - now
                problems = Contest_problem.objects.filter(contest__id = cid).order_by('num')
                username = request.user.username

                hours = int(start_time / (60 * 60))
                minutes = int((start_time - (hours * 60 * 60)) / 60)
                seconds = int(start_time - (hours * 60 * 60) - (minutes * 60))
                try:
                    user_authority = Privilege.objects.get(user__user__username = username).authority
                    if user_authority == config.ADMIN or contest.user.user.username == username:
                        start_time = 0
                    else:
                        if contest.private == 1:
                            if contest.visible == False:
                                error= "Limited permission!"
                                return render(request, "error.html", {'error': error})
                            else:
                                try:
                                    ContestPrivilege.objects.get(user__user__username = username, contest__id = contest.id)
                                except ObjectDoesNotExist:
                                    error= "Limited permission!"
                                    return render(request, "error.html", {'error': error})
                        else:
                            if contest.visible == False and user_authority != config.ADMIN and contest.user.user.username != username:
                                error = "Limited permission!"
                                return render(request, "error.html", {'error': error})
                except ObjectDoesNotExist:
                    if contest.user.user.username == username:
                        start_time = 0
                    else:
                        if contest.private == 1:
                            if contest.visible == False:
                                error = "Limited permission!"
                                return render(request, "error.html", {'error': error})
                            else:
                                try:
                                    ContestPrivilege.objects.get(user__user__username = username, contest__id = contest.id)
                                except ObjectDoesNotExist:
                                    error= "Limited permission!"
                                    return render(request, "error.html", {'error': error})
                        else:
                            if contest.visible == False and user_authority != config.ADMIN and contest.user.user.username != username:
                                error = "Limited permission!"
                                return render(request, "error.html", {'error': error})
                contest_user = False
                if username == contest.user.user.username:
                    contest_user = True
                ADMIN = False
                if user_authority == config.ADMIN:
                    ADMIN = True
                problem_dict = {'problems': problems, 'contest': contest, 'start_time': int(start_time),\
                                'ADMIN': ADMIN, 'contest_user': contest_user, 'cid': cid, 'hours': hours, 'minutes': minutes, 'seconds': seconds}
                return render(request, 'contest/contest_problem_list.html', problem_dict)

            except ObjectDoesNotExist:
                error= "This contest does not exist!"
                return render(request, "error.html", {'error': error})
            
            '''
            if request.user.is_authenticated():
                solution_list = Solution.objects.filter(user_id = request.user.id, contest_id = cid)
                accepted = solution_list.filter(result=4).order_by('problem').\
                        values_list('problem', flat=True).distinct()
                unsolved = solution_list.exclude(result=4).order_by('problem').\
                        values_list('problem', flat=True).distinct()
                problem_dict['accepted'] = accepted
                problem_dict['unsolved'] = unsolved
                print accepted, unsolved
            '''


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
                    if last_solution.pass_rate == None:
                        last_solution.pass_rate = 0
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
                                                  'page': int(page),
                                                  'cid': cid})
