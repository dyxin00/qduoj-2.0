from django.db import models
#from oj_user.models import User

class Problem(models.Model):
    title = models.CharField(max_length = 200, default = '')
    description = models.TextField()
    pro_input = models.TextField()
    pro_output = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    spj = models.CharField(max_length = 1, default = '0') #max_length
    hint = models.TextField()
    source = models.CharField(max_length = 100, null = True)
    in_date = models.DateTimeField(null = True)
    time_limit = models.IntegerField(default = 0)
    memory_limit = models.IntegerField(default = 0)
    defunct = models.BooleanField(default = False)
    accepted = models.IntegerField(default = 0)
    submit = models.IntegerField(default = 0)
    solved = models.IntegerField(default = 0)
  # user = models.ForeignKey(User)
