from django.shortcuts import render
from solution.models import Solution

def solution_list(request):
    if request.method=="GET":
        judge_list = Solution.objects.all().order_by('-in_date')
        return render(request, "solution/status.html", 
            {'judge_list': judge_list})
    return render(request, "solution/status.html", {})
