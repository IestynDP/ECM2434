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

#holds base information about items
class items(models.Model):
    itemid = models.AutoField(primary_key=True)
    itemName = models.CharField(max_length=100,default="")
    itemCost = models.IntegerField(default = 20)
    itemimage = models.CharField(max_length=500,default="ItemImage")
    itemslot = models.CharField(max_length=50, default="")

#holds which items a user has purchased
class purchases(models.Model):
    user = models.ForeignKey(account,on_delete=models.CASCADE)
    item = models.ForeignKey(items,on_delete=models.CASCADE)
    equipState = models.BooleanField(default=False)


