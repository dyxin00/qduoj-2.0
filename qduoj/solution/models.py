from django.db import models
from problem.models import Problem
from oj_user.models import User

class Solution(models.Model):
    solution_id = models.IntegerField()
    problem = models.ForeignKey(Problem, primary_key = True)
    user = models.ForeignKey(User)
    time = models.IntegerField(default = 0)
    memory = models.IntegerField(default = 0)
    in_date = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(default = 0)
    language = models.IntegerField(default = 0)
    ip = models.CharField(max_length = 15)
    contest_id = models.IntegerField(null =True)
    valid = models.IntegerField(default = 1)
    num = models.IntegerField(default = -1)
    code_length = models.IntegerField(default = 0)
    judgetime = models.DateTimeField(null = True)
    pass_rate = models.DecimalField(max_digits = 2, decimal_places = 2)
    ######

class Compileinfo(models.Model):
    solution = models.ForeignKey(Solution, primary_key = True)
    error = models.TextField()

class Custominput(models.Model):
    solution = models.ForeignKey(Solution, primary_key = True)
    input_text = models.TextField()
