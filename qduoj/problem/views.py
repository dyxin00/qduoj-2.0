# -*- coding: utf-8 -*-    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from problem.models import Problem

def index(request):
    if request.method == 'GET':

        problem_type = request.GET.get('type', '-1')

        if problem_type == '-1':
            problems = Problem.objects.all()

        else:
            problems = Problem.objects.filter(classify=problem_type)

        return render(request, "problem/problem_list.html",
                {'problems': problems, 'type' : problem_type})
    

def problem(request):
    return render(request,"problem/problem.html", {})


@login_required(login_url='sign_in')
def submit_code(request):

    if request.method == 'POST':

        code = request.POST.get('code', '')
        language = request.POST.get('language', '')
        pid = request.POST.get('pid', '')
        # 未验证数据正确性

        return redirect('status_list')

    return redirect('index')
