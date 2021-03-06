from django.db import models
from django.contrib.auth.models import User
class User_oj(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    submit = models.IntegerField(default=0)
    solved = models.IntegerField(default=0)
    school_id = models.CharField(max_length=12)
    reg_time = models.DateField(auto_now=True)
    accesstime = models.DateField(null=True)
    integral = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.user.username

    class Meta:
        db_table = "users"
        ordering = ['-solved', 'submit']

class Privilege(models.Model):
    user = models.ForeignKey(User_oj)
    authority = models.IntegerField()
    defunct = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.user.username + ' - authority - ' + str(self.authority)

    class Meta:
        db_table = "privilege"

    #alter table test AUTO_INCREMENT = 1000;
