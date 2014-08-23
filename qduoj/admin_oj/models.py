from django.db import models

class Auditing(models.Model):

    auditing_key = models.CharField(max_length=50, primary_key=True)
    auditing_value = models.CharField(max_length=50)
    desc = models.TextField()

    class Meta:
        db_table = 'auditing'
