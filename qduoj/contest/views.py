from django.shortcuts import render, redirect

def contest_list(request):

    return render(request, 'contest/contest_list.html', {})
