#!/usr/bin/python
# coding=utf-8

from functools import wraps
from admin_oj.models import Auditing
from oj_user.models import User_oj, Privilege

def Authorization(auditing):

    def _Authorization(func):

        @wraps(func)
        def wrapped(request, *args, **kargs):
            return func(request, *args, **kargs)
        return wrapped
    return _Authorization


