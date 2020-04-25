from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=50, default='')
    join_id = models.BigIntegerField(null=True)
    users = models.ManyToManyField(to=User)
    join_id = models.BigIntegerField(null=True)

