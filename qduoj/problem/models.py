  # -*- coding: utf-8 -*-
from django.db import models
from oj_user.models import User_oj

class Problem(models.Model):
    title = models.CharField(max_length=200, default='')
    description = models.TextField()
    pro_input = models.TextField()
    pro_output = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    spj = models.CharField(max_length=1, default='0')
    hint = models.TextField(null=True)
    source = models.CharField(max_length=100, null=True)
    in_date = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=0)
    memory_limit = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    #过时的
    defunct = models.BooleanField(default=False)
    #标程
    accepted = models.IntegerField(default=0)
    #分类
    classify = models.IntegerField(default=0)
    submit = models.IntegerField(default=0)
    solved = models.IntegerField(default=0)
    user = models.ForeignKey(User_oj)
    difficult = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.id) + ' - '+ self.title + ' - ' + self.user.user.username

    class Meta:
        db_table = "problem"


class Score(models.Model):
    problem = models.ForeignKey(Problem)
    file_name = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    
    def __unicode__(self):
        return str(self.problem.id) + ' - ' + self.problem.title + ' - ' + str(self.score)
    class Meta:
        db_table = "score"
        unique_together = (("problem", "file_name"),)

class Problem_Image(models.Model):
    problem = models.ForeignKey(Problem)
    image = models.ImageField(upload_to='/')

    class Meta:
        db_table = 'image'
