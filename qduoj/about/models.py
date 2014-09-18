from django.db import models
from oj_user.models import User_oj

class News(models.Model):
    user = models.ForeignKey(User_oj)
    title = models.CharField(max_length=200, default='')
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=False)
    classify = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id) + ' - ' + self.title + ' - ' + self.user.user.username
    
    class Meta:
        db_table = 'news'
        ordering = ['-id']
