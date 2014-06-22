  # -*- coding: utf-8 -*-
from django.db import models
from oj_user.models import User

class Problem(models.Model):
    title = models.CharField(max_length=200, default='')
    description = models.TextField()
    pro_input = models.TextField()
    pro_output = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    spj = models.CharField(max_length=1, default='0')
    hint = models.TextField()
    source = models.CharField(max_length=100, null=True)
    in_date = models.DateTimeField(null=True)
    time_limit = models.IntegerField(default=0)
    memory_limit = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    #过时的
    defunct = models.BooleanField(default=False)
    #标程
    accepted = models.IntegerField(default=0)
    submit = models.IntegerField(default=0)
    solved = models.IntegerField(default=0)
    user = models.ForeignKey(User)

class Score(models.Model):
    problem_id = models.ForeignKey(Problem, primary_key=True)
    score = models.IntegerField(default=0)    
