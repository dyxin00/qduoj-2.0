# -*- coding: utf-8 -*-  
from random import choice
import re
import time, datetime
import json
import os
from  PIL import ImageFile

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from DjangoVerifyCode import Code
from django.core.exceptions import ObjectDoesNotExist
from oj_user.models import User_oj, Privilege
from problem.models import Problem
from solution.models import Solution
from admin_oj.models import Check_problem_contest
from django.db.models import Sum, Q
from qduoj import config
from qduoj.config import *

from admin_oj.util import Authorization

@Authorization(ADD_PRO)
def get_check_list(request, *arges, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    values = {'cpid', 'check', 'user__user__username', 'desc'}
    check_list = Check_problem_contest.objects.select_related(depth=3).all().values(*values)
    response_dict['check_list'] = list(check_list)
    del response_dict['user']
    return HttpResponse(json.dumps(response_dict), content_type="application/json")

@Authorization(ADD_PRO)
def check_save(request, *args, **kwargs):
    cpid = request.GET.get('id')
    obj = Check_problem_contest.objects.get(cpid=cpid)
    obj.check = request.GET.get('check')
    obj.desc = request.GET.get('desc')
    obj.save()
    return HttpResponse(json.dumps({'status': 200}), content_type="application/json")
