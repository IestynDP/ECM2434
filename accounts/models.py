from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(default=" ")

    def __str__(self):
        return self.user.username

class tasks(models.Model):
    taskID = models.IntegerField(primary_key=True)
    #tasks