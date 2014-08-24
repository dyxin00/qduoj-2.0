from django.shortcuts import render
from admin_oj.util import Authorization

@Authorization('')
def index(request):

    return render(request, 'admin_oj/base.html', {})
