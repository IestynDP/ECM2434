from django.db import models

# Create your models here.
class account(models.Model):
    userId = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    points = models.IntegerField()
    accountType = models.CharField(max_length=10)
    # profile picture

class tasks(models.Model):
    taskID = models.IntegerField(primary_key=True)
    #tasks 