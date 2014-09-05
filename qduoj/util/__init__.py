# -*- coding: utf-8 -*-   
import functools
from django.shortcuts import render

def request_method_only(method):
    def _request_method_only(func):

        @functools.wraps(func)
        def wrapped(request):
            if request.method != method:

                error = "~ ~呵呵！！"
                return render(request, "error.html", {'error':error})
            return func(request)
        return wrapped
    return _request_method_only
