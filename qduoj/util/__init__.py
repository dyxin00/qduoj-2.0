# -*- coding: utf-8 -*-   

from django.shortcuts import render

def request_method_only(method):
    def _request_method_only(fun):

        def wrapped(request):
            if request.method != method:

                error = "~ ~呵呵！！"
                return render(request, "error.html", {'error':error})
            return fun(request)
        return wrapped
    return _request_method_only
