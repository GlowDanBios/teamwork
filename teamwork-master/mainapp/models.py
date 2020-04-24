from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=50, default='')
    users = models.ManyToManyField(to=User)
