# -*- coding: utf-8 -*-
from django.db import models
from oj_user.models import User_oj
from problem.models import Problem

class Contest(models.Model):
    title = models.CharField(max_length=255, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    defunct = models.BooleanField(default=False)
    description = models.TextField()
    private = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    langmask = models.IntegerField(default=0)
    #mode 0 -> acm, 1->OI
    mode = models.IntegerField(default=0)
    user = models.ForeignKey(User_oj)
    
    def __unicode__(self):
        return str(self.id) + ' - ' + self.title + ' - ' + self.user.user.username

    class Meta:
        db_table = 'contest'

class Contest_problem(models.Model):
    problem = models.ForeignKey(Problem)
    contest = models.ForeignKey(Contest)
    title = models.CharField(max_length=200, default='')
    num = models.IntegerField(default=0)
    sorce = models.IntegerField()
    
    def __unicode__(self):
        return str(self.id) + ' - ' + self.problem.title + ' - ' + str(self.problem.id)
    
    class Meta:
        db_table = 'contest_problem'

class ContestPrivilege(models.Model):
    user = models.ForeignKey(User_oj)
    contest = models.ForeignKey(Contest)
