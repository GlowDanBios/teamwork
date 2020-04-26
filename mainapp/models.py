from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=50, default='')
    join_id = models.BigIntegerField(null=True)
    users = models.ManyToManyField(to=User)
    code = models.TextField(default='', null=True)


class Message(models.Model):
    text = models.TextField(default='', null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.TimeField(auto_now_add=True)


class Task(models.Model):
    text = models.TextField(default='', null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)


class File(models.Model):
    file = models.FileField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
