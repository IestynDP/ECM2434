from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField

# Create your models here.
class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class tasks(models.Model):
    taskID = models.IntegerField(primary_key=True)

#holds base information about items
class items(models.Model):
    itemid = models.AutoField(primary_key=True)
    itemName = models.CharField(max_length=100,default="")
    itemCost = models.IntegerField(default = 20)
    itemimage = models.CharField(max_length=500,default="ItemImage")
    itemslot = ["hat","shirt","glasses"]

#holds which items a user has purchased
class purchases(models.Model):
    user = models.ForeignKey(account,on_delete=models.CASCADE)
    item = models.ForeignKey(items,on_delete=models.CASCADE)
    equipState = models.BooleanField(default=False)

    #tasks
    
class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Business owner
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    sustainability_features = models.TextField()
    verified = models.BooleanField(default=False)  # Will be used for verification later

    def __str__(self):
        return self.name

class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who checked in
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # Where they checked in
    timestamp = models.DateTimeField(auto_now_add=True)  # When they checked in

    class Meta:
        unique_together = ('user', 'restaurant', 'timestamp')  # Prevent duplicate check-ins per day

    def __str__(self):
        return f"{self.user.username} checked into {self.restaurant.name}"