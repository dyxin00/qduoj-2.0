# -*- coding: utf-8 -*-  
import re
import json

from django.http import HttpResponse
from django.forms.models import model_to_dict

from django.core.exceptions import ObjectDoesNotExist
from about.models import News
from oj_user.models import User_oj

from qduoj.config import *

from admin_oj.util import Authorization

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def get_news_list(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    page = int(request.GET.get('page', 0))
    

    index_start = page * PAGE_COUNT
    index_end = (page + 1) * PAGE_COUNT
    check = {}
    info = ('id', 'title', 'user__user__username', 'visible') #change time type 
    news_list = News.objects.filter(**check).values(*info)
    all_count = News.objects.all().count()
    count = news_list.count() 

    last_page = False
    if index_end > count:
        index_end = count
        last_page = True

    if index_end == all_count:
        last_page = True

    news_list = news_list[index_start : index_end]
    response_dict['news_list'] = list(news_list)
    response_dict['last_page'] = last_page
    del response_dict['user']
    return HttpResponse(json.dumps(response_dict), content_type='application/json')

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def news_add(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    username = request.user.username

    user = User_oj.objects.get(user__username=username)
    key_news = {
        'user' : user,
        'title' : request.POST.get('title', ''),
        'description' : request.POST.get('desc', ''),
        'classify' : request.POST.get('classify', '0')
    }

    try:
        News.objects.create(**key_news)
    except:
        return HttpResponse(json.dumps({'status':503}), content_type='application/json') 
    return HttpResponse(json.dumps({'status':200}), content_type='application/json')


@Authorization(ADD_CON_AND_PRO_AND_VIS)
def news_visible(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    news_id = request.GET.get('news_id', '')

    if not re.match(ur'[0-9]+$', unicode(news_id)):
        return HttpResponse(json.dumps({'status':400}), content_type='application/json')

    try:
        news = News.objects.get(id=news_id)
    except:
        return HttpResponse(json.dumps({'status':503}), content_type='application/json')

    news.visible = not news.visible
    try:
        news.save()
    except:
        return HttpResponse(json.dumps({'status':503}), content_type='application/json')

    return HttpResponse(json.dumps({'status':200}), content_type='application/json')

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def news_delete(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    news_id = request.GET.get('news_id', '')
    
    if not re.match(ur'[0-9]+$', unicode(news_id)):
        return HttpResponse(json.dumps({'status':400}), content_type='application/json') 

    try:
        news = News.objects.get(id=news_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status':400}), content_type='application/json') 
    
    try:
        news.delete()
    except:
        return HttpResponse(json.dumps({'status':503}), content_type='application/json') 
    return HttpResponse(json.dumps({'status':200}), content_type='application/json')


@Authorization(ADD_CON_AND_PRO_AND_VIS)
def news_get(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    news_id = request.GET.get('news_id', '')

    if not re.match(ur'[0-9]+$', unicode(news_id)):
        return HttpResponse(json.dumps({'status':400}), content_type='application/json') 
    
    try:
        news = News.objects.get(id=news_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status':400}), content_type='application/json') 
    
    response_dict['news'] = model_to_dict(news)
    response_dict['status'] = 200

    del response_dict['user']
    return HttpResponse(json.dumps(response_dict), content_type='application/json')

@Authorization(ADD_CON_AND_PRO_AND_VIS)
def news_modify(request, *args, **kwargs):
    response_dict = kwargs.get('response_dict', {})
    news_id = request.POST.get('id', '')
    print news_id

    if not re.match(ur'[0-9]+$', unicode(news_id)):
        return HttpResponse(json.dumps({'status':400}), content_type='application/json') 

    username = request.user.username
    user = User_oj.objects.get(user__username=username)

    news_modify = News.objects.get(id=news_id)
    news_modify.user = user
    news_modify.title = request.POST.get('title', '')
    news_modify.description = request.POST.get('desc', '')
    news_modify.classify = request.POST.get('classify', '0')
    try:
        news_modify.save()
    except:
        return HttpResponse(json.dumps({'status':503}), content_type='application/json') 

    return HttpResponse(json.dumps({'status':200}), content_type='application/json')

def news_show(request):
    news_list = News.objects.filter(visible=True)
    response_dict = {}
    try:
        news = news_list[0]
        response_dict['news'] = model_to_dict(news)
        response_dict['status'] = 'success'
    except:
        response_dict['status'] = 'filed'

    return HttpResponse(json.dumps(response_dict))

