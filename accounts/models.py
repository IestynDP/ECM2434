from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(default=" ")

class tasks(models.Model):
    taskID = models.IntegerField(primary_key=True)
    #tasks
class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Business owner
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255)  # Address or general location
    sustainability_features = models.TextField(help_text="List what makes this restaurant eco-friendly.")
    verified = models.BooleanField(default=False)  # Will be used for verification later

    def __str__(self):
        return self.name