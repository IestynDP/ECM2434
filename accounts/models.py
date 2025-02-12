from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

class tasks(models.Model):
    taskID = models.IntegerField(primary_key=True)
    #tasks