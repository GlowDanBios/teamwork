from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=50, default='')
    users = models.ManyToManyField(to=User)
    join_id = models.BigIntegerField(null=True)

