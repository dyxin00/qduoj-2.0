from django.db import models
from oj_user.models import User_oj
from problem.models import Problem
from contest.models import Contest
import time, datetime
from django.utils import timezone

class Auditing(models.Model):

    auditing_key = models.CharField(max_length=50, primary_key=True)
    auditing_value = models.CharField(max_length=50)
    desc = models.TextField()

    class Meta:
        db_table = 'auditing'

class Check(models.Model):
    cpid = models.CharField(max_length=20, primary_key=True)
    check = models.IntegerField(default=0)
    user = models.ForeignKey(User_oj)
    desc = models.TextField(null=True)
    in_date = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'check'

    def __unicode__(self):
        return self.cpid + ' - ' + self.check
 
class Check_problem_contest(models.Model):
    cpid = models.CharField(max_length=20, primary_key=True)
    check = models.IntegerField(default=0)
    user = models.ForeignKey(User_oj)
    desc = models.TextField(null=True, default='')
    in_date = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'Check_problem_contest'

    def __unicode__(self):
        return self.cpid + ' - ' + str(self.check)
   
