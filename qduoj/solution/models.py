# -*- coding: utf-8 -*-
from django.db import models
from problem.models import Problem
from contest.models import Contest
from oj_user.models import User_oj

class Solution(models.Model):
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(User_oj)
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    in_date = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(default=0)
    language = models.IntegerField(default=0)
    ip = models.CharField(max_length=15)
    contest = models.ForeignKey(Contest, null=True)
    valid = models.IntegerField(default=1)
    num = models.IntegerField(default=-1)
    code_length = models.IntegerField(default=0)
    judgetime = models.DateTimeField(null=True)
    pass_rate = models.DecimalField(max_digits=2, decimal_places=2, null=True)
    ######

    class Meta:
        db_table = 'solution'
    def __unicode__(self):
        return str(self.problem.id) + ' - ' + self.problem.title + ' - ' + self.user.user.username

class Compileinfo(models.Model):
    solution = models.ForeignKey(Solution, primary_key=True)
    error = models.TextField()

    class Meta:
        db_table = 'compileinfo'
class Custominput(models.Model):
    solution = models.ForeignKey(Solution, primary_key=True)
    input_text = models.TextField()

    class Meta:
        db_table = 'custominput'
class Runtimeinfo(models.Model):
    solution = models.ForeignKey(Solution)
    error = models.TextField()

    class Meta:
        db_table = 'runtimeinfo'

class Source_code(models.Model):
    solution = models.ForeignKey(Solution)
    source  = models.TextField()

    class Meta:
        db_table = 'source_code'
