from django.db import models
from oj_user.models import User
from problem.models import Problem
from solution.models import Solution

class Contest(models.Model):
    title = models.CharField(max_length = 255, null =True)
    start_time = models.DateTimeField(null =True)
    end_time = models.DateTimeField(null = True)
    defunct = models.BooleanField(default = False)
    description = models.TextField()
    private = models.IntegerField(default = 0)
    langmask = models.IntegerField(default = 0)
    user = models.ForeignKey(User)

class Contest_problem(models.Model):
    problem_id = models.ForeignKey(Problem)
    title = models.CharField(max_length = 200, default = '')
    num = models.IntegerField(default = 0)

class Runtimeinfo(models.Model):
    solution_id = models.ForeignKey(Solution)
    error = models.TextField()
