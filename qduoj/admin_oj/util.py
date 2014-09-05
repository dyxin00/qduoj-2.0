#!/usr/bin/python
# coding=utf-8

import json
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import render
from admin_oj.models import Auditing
from django.core.exceptions import ObjectDoesNotExist

from oj_user.models import User_oj, Privilege

def Authorization(*args):

    def _Authorization(func):

        @wraps(func)
        def wrapped(request):
            response_dict = {}
            user_oj = request.user.user_oj
            try:
                privilege = Privilege.objects.get(user=user_oj).authority
            except ObjectDoesNotExist:
                return HttpResponse(json.dumps({'status': '412'}))
            response_dict['privilege'] = privilege
            response_dict['user'] = user_oj
            for val in args:
                if val & privilege == 0 or val & privilege != val:
                    return HttpResponse(json.dumps({'status': '412'}))
            return func(request, response_dict=response_dict)
        return wrapped
    return _Authorization

