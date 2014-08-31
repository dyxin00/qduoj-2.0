from django.shortcuts import render, redirect
from problem.models import Problem, Score
from contest.models import Contest, Contest_problem, ContestPrivilege
from solution.models import Solution, Custominput, Source_code
from oj_user.models import User_oj, Privilege
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from xlwt import Workbook
from StringIO import StringIO
import time, datetime
from qduoj import config

def contest_list(request):
    if request.method == 'GET':
        status = request.GET.get('status', -1)
        username = request.user.username
        try:
            user_authority = Privilege.objects.get(user__user__username=username).authority
            if user_authority == config.ADMIN:
                contests = Contest.objects.all()
            else:
                contests = Contest.objects.select_related(depth=3).filter(Q(visible=True) | (Q(user__user__username=username) & Q(visible=False)))

        except ObjectDoesNotExist:
            contests = Contest.objects.select_related(depth=3).filter(Q(visible=True) | (Q(user__user__username=username) & Q(visible=False)))
        for contest in contests:
            if (contest.start_or_not() == True and contest.end_or_not() == True) or (contest.start_or_not() == False):
                if contest.defunct:
                    contest.defunct = False
                    contest.save()
            else:
                if contest.defunct == False:
                    contest.defunct = True
                    contest.save()
        if status == '1':
            contests = contests.select_related(depth=3).filter(defunct=False)
        else:
            contests = contests.select_related(depth=3).filter(defunct=True)
        return render(request, 'contest/contest_list.html', {'contests': contests})

def contest_problem_list(request):
    if request.method == 'GET':
        cid = request.GET.get('cid', None)
        if cid != None:
            try:
                contest = Contest.objects.get(id=cid)
                now = time.time()
                t1 = contest.start_time.replace(tzinfo=None) + datetime.timedelta(hours=8)
                t2 = contest.end_time.replace(tzinfo=None) + datetime.timedelta(hours=8)
                start_time = float(time.mktime(time.strptime(str(t1),
                                            '%Y-%m-%d %H:%M:%S'))) - now
                end_time = float(time.mktime(time.strptime(str(t2),
                                             '%Y-%m-%d %H:%M:%S'))) - now
                problems = Contest_problem.objects.select_related(depth=3).filter(contest__id=cid).order_by('num')
                username = request.user.username

                hours = int(start_time / (60 * 60))
                minutes = int((start_time - (hours * 60 * 60)) / 60)
                seconds = int(start_time - (hours * 60 * 60) - (minutes * 60))
                ADMIN = False
                try:
                    user_authority = Privilege.objects.get(user__user__username=username).authority
                    if user_authority == config.ADMIN:
                        ADMIN = True
                    if user_authority == config.ADMIN or contest.user.user.username == username:
                        start_time = 0
                    else:
                        if contest.private == 1:
                            if contest.visible == False:
                                error= "Limited permission!"
                                return render(request, "error.html", {'error': error})
                            else:
                                try:
                                    ContestPrivilege.objects.get(user__user__username=username, contest__id=contest.id)
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
                                    ContestPrivilege.objects.get(user__user__username=username, contest__id=contest.id)
                                except ObjectDoesNotExist:
                                    error = "Limited permission!"
                                    return render(request, "error.html", {'error': error})
                        else:
                            if contest.visible == False and user_authority != config.ADMIN and contest.user.user.username != username:
                                error = "Limited permission!"
                                return render(request, "error.html", {'error': error})
                contest_user = False
                if username == contest.user.user.username:
                    contest_user = True
                accepted = []
                unsolved = []
                if request.user.is_authenticated():
                    solution_list = Solution.objects.select_related(depth=3).filter(user_id=request.user.id, contest_id=cid)
                    accepted = solution_list.filter(result=4).order_by('problem').\
                            values_list('problem', flat=True).distinct()
                    unsolved = solution_list.exclude(result=4).order_by('problem').\
                            values_list('problem', flat=True).distinct()
                problem_dict = {'problems': problems, 'contest': contest, 'start_time': int(start_time),
                                'ADMIN': ADMIN, 'contest_user': contest_user, 'cid': cid, 'hours': hours, 
                                'minutes': minutes, 'seconds': seconds, 'flag': contest.end_or_not(), 
                                'contest_title': contest.title, 'accepted': accepted, 'unsolved': unsolved}
                    
                return render(request, 'contest/contest_problem_list.html', problem_dict)
            
            except ObjectDoesNotExist:
                error = "This contest does not exist!"
                return render(request, "error.html", {'error': error})
            

def contest_rank(request):
    if request.method == 'GET':
        cid = request.GET.get('cid', None)
        page = request.GET.get('page', '1')
        xls = request.GET.get('xls', 'None')

        if cid == None:
            error = "The contest is not exist!"
            return render(request, 'error.html', {'error': error})
         
        try:
            contest = Contest.objects.get(id=cid)
        except ObjectDoesNotExist:
            error = "The contest is not exist!"
            return render(request, 'error.html', {'error':error})

	contest_user_id_list = Solution.objects.select_related(depth=3).filter(contest__id=cid).\
                order_by('user__user__id').values_list('user__user__id', flat=True).distinct()
        contest_user_list = User_oj.objects.filter(user__id__in=contest_user_id_list)
        
        contest_problem_list = Contest_problem.objects.select_related(depth=3).filter(contest__id=cid).order_by('num')
        solutions = Solution.objects.select_related(depth=3).all().filter(contest__id=cid)

        if contest.mode == 1:
            return contest_rank_oi(request, contest, cid, xls, page, contest_user_list, contest_problem_list, solutions)
        else:
            return contest_rank_acm(request, contest, cid, xls, page, contest_user_list, contest_problem_list, solutions)
            

def contest_rank_oi(request, contest, cid, xls, page, contest_user_list, contest_problem_list, solutions):
  
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
                    last_solution = solutions.filter(problem__id=problem.problem.id, user__user__id=contest_user.user.id).order_by('-id')[0]
                    if last_solution.pass_rate == None:
                        last_solution.pass_rate = 0
                    problem_score = float(last_solution.pass_rate) * problem.sorce
                    if problem_score == problem.sorce:
                        accepted += 1
                        problem_loop['AC'] = True
                    else:
                        problem_loop['AC'] = False
                    problem_loop['score'] = problem_score
                    problem_loop['submit'] = solutions.filter(problem__id=problem.problem.id, user__user__id=contest_user.user.id).count()
                    grade += problem_score

                except IndexError:
                    problem_loop['AC'] = False
                    problem_loop['score'] = 0.0
                    problem_loop['submit'] = -1
                    grade += 0
                problem_info.append(problem_loop)
                    
            contest_user_loop.append(grade)
            contest_user_loop.append(accepted)
            contest_user_loop.append(solutions.filter(user__user__id=contest_user.user.id).count())
            contest_user_loop.append(problem_info)
            
            contest_info.append(contest_user_loop)
        contest_info.sort(key=lambda t: (t[1], t[2], -t[3]), reverse=True)
        if xls == 'None':
            return render(request, 'rank/rank.html', {'user_list': contest_info,
                                                     'mode': contest.mode,
                                                     'page': int(page),
                                                     'cid': cid,
                                                     'contest_problem': contest_problem_list,
                                                     'contest_title': contest.title})
        else:
            return contest_rank_xls_oi(contest_info, contest, cid, contest_problem_list)

def contest_rank_acm(request, contest, cid, xls, page, contest_user_list, contest_problem_list, solutions):
    contest_time = contest.start_time
    contest_info = []
    for contest_user in contest_user_list:
        accepted = 0
        user_problem = []
        total_time = datetime.timedelta()
        
        for problem in contest_problem_list:
            all_solution = solutions.filter(problem__id=problem.problem.id, user__user__id=contest_user.user.id)
            ac_solution = all_solution.filter(result=4).order_by("id")

            unsolved_num = all_solution.exclude(result=4).count()

            if ac_solution:
                ac_time = ac_solution[0].in_date - contest_time
                wise_time = datetime.timedelta(minutes=unsolved_num * 20)
                user_problem.append({
                    'submit': 1,
                    'ac_time': ac_time,
                    'unsolved': unsolved_num
                })
                total_time = total_time + ac_time + wise_time
                accepted += 1
            else:
                user_problem.append({
                    'submit': 0,
                    'unsolved': unsolved_num
                })
        contest_loop = []
        contest_loop.append(contest_user.user.username)
        contest_loop.append(accepted)
        contest_loop.append(total_time)
        contest_loop.append(user_problem)

        contest_info.append(contest_loop)
    contest_info.sort(key=lambda t: (-t[1], t[2]))
    if xls == 'None':
        return render(request, 'rank/rank.html', {'user_list': contest_info,
                                                  'mode': contest.mode,
                                                  'page': int(page),
                                                  'cid': cid,
                                                  'contest_problem': contest_problem_list,
                                                  'contest_title': contest.title})
    else:
        return contest_rank_xls_acm(contest_info, contest, cid, contest_problem_list)

def contest_rank_xls_oi(contest_info, contest, cid, contest_problem_list):
    wbk = Workbook(encoding='utf-8') 
    sheet = wbk.add_sheet(u"contest-score-%s" %contest.title)
    sheet.write(0, 0, u"-------Contest-score-%s-------" %contest.title)
    sheet.write(1, 0, u"Rank") 
    sheet.write(1, 1, u"User") 
    sheet.write(1, 2, u"Grade")
    line = 3
    for title in contest_problem_list:
        sheet.write(1, line, u"%s"%title.title)
        line += 1
    sheet.write(1, line, u"Solved") 
    line += 1
    sheet.write(1, line, u"Submit")
    line = 2
    for var in contest_info:
        sheet.write(line, 0, u"%s"%str(line - 1))
        sheet.write(line, 1, u"%s"%var[0])
        sheet.write(line, 2, u"%s"%var[1])
        count1 = 3
        for problem in var[4]:
            print problem['submit']
            if problem['submit'] != '-1':
                sheet.write(line, count1, u"%s"%problem['score'])
            else:
                sheet.write(line, count1, u" ")
            count1 += 1
        sheet.write(line, count1, u"%s"%var[2])
        count1 += 1
        sheet.write(line, count1, u"%s"%var[3])
        line += 1
    
    ios = StringIO()
    wbk.save(ios)
    response = HttpResponse(ios.getvalue(), mimetype='application/ontet-stream')
    response['Content-Disposition'] = 'attachment; filename=contest-%s.xls'% cid
    return response

def contest_rank_xls_acm(contest_info, contest, cid, contest_problem_list):
    wbk = Workbook(encoding='utf-8')
    sheet = wbk.add_sheet(u"contest-score-%s" %contest.title)
    sheet.write(0, 0, u"-------Contest-score-%s-------" %contest.title)
    sheet.write(1, 0, u"Rank")
    sheet.write(1, 1, u"User")
    sheet.write(1, 2, u"AC")
    sheet.write(1, 3, u"Time")
    line = 4
    for title in contest_problem_list:
        sheet.write(1, line, u"%s"%title.title)
        line += 1
    line = 2
    for var in contest_info:
        if line == 2:
            sheet.write(line, 0, u"%s"%"Winner")
        else:
            sheet.write(line, 0, u"%s"%str(line-1))
        sheet.write(line, 1, u"%s"%var[0])
        sheet.write(line, 2, u"%s"%var[1])
        sheet.write(line, 3, u"%s"%var[2])
        count = 4
        for problem in var[3]:
            if problem['submit'] == 1:
                if problem['unsolved'] != 0:
                    sheet.write(line, count, u"%s-(%s)"%(problem['ac_time'], problem['unsolved']))
                else:
                    sheet.write(line, count, u"%s"%problem['ac_time'])
            else:
                if problem['unsolved'] != 0:
                    sheet.write(line, count, u"-(%s)"%problem['unsolved'])
            count += 1
        line += 1

    ios = StringIO()
    wbk.save(ios)
    response = HttpResponse(ios.getvalue(), mimetype='application/ontet-stream')
    response['Content-Disposition'] = 'attachment; filename=contest-%s.xls'% cid
    return response

