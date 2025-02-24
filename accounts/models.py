from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField



# Create your models here.
class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = EncryptedCharField(max_length=500, default=" ")

class tasks(models.Model):
    taskID = models.IntegerField(primary_key=True)
    #tasks