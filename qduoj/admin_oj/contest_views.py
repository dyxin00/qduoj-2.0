# -*- coding: utf-8 -*-  
from random import choice
import re
import time, datetime
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from DjangoVerifyCode import Code
from django.core.exceptions import ObjectDoesNotExist
from oj_user.models import User_oj, Privilege
from problem.models import Problem
from contest.models import Contest
from solution.models import Solution

from django.db.models import Sum, Q
from qduoj import config
from qduoj.config import *

from admin_oj.util import Authorization

@Authorization(ADD_PRO)
def get_contest_list(request, *args, **kwargs):
    request_dict = kwargs.get('request_dict', {})
    page = int(request.GET.get('page', 0))
    count = Contest.objects.all().count()
    index_start = page * PAGE_COUNT
    index_end = (page + 1) * PAGE_COUNT

    if index_end > count:
        index_end = count
    check = {'visible': True}
    info = ('id', 'title', 'user__user__username', 'visible')
    contest_list = Contest.objects.filter(**check)[index_start : index_end].values(*info)
    request_dict['contest_list'] = list(contest_list)
    return HttpResponse(json.dumps(request_dict), content_type="appliction/json")

