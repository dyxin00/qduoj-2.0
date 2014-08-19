from django.shortcuts import render, redirect
from problem.models import Problem
from contest.models import Contest

def contest_list(request):
    contests = Contest.objects.filter(visible=True)
    return render(request, 'contest/contest_list.html', {'contests': contests})

