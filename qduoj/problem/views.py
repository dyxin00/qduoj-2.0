from django.shortcuts import render

def index(request):

    return render(request,"problem/problem_list.html", {})
def problem(request):

    return render(request,"problem/problem.html", {})
