from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=50, default='')
    join_id = models.BigIntegerField(null=True)
    users = models.ManyToManyField(to=User)

class Message(models.Model):
    text = models.TextField(default='', null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.TimeField(auto_now_add=True)
