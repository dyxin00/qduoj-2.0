from django.shortcuts import render


def solution_list(request):
    return render(request, "solution/status.html", {})
