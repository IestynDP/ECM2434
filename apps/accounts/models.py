import random, string
from django.db import models, connection
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from encrypted_model_fields.fields import EncryptedCharField
from django.utils import timezone
from .utils import generate_unique_qr_code
import qrcode
from io import BytesIO 
import base64

# Create your models here.
class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0) # Current points
    total_points = models.IntegerField(default=0)  # Total lifetime points
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
    itemimage = models.ImageField(upload_to="items/")
    itemslot = models.CharField(max_length=20)

#holds which items a user has purchased
class purchases(models.Model):
    user = models.ForeignKey(account,on_delete=models.CASCADE)
    item = models.ForeignKey(items,on_delete=models.CASCADE)
    equipState = models.BooleanField(default=False)

    #tasks


# Allows adding restaurants
class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Business owner
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    sustainability_features = models.TextField()
    verified = models.BooleanField(default=False)
    qrCodeID = models.CharField(max_length=16, unique=True, default=generate_unique_qr_code)
    points = models.IntegerField(default=10)  # Points for checking in

    def __str__(self):
        return self.name
    
    def qr_code_base64(self):
        # Create QR code image
        qr = qrcode.make(self.qrCodeID)  # You can change this to any field of the restaurant
        buffered = BytesIO()
        qr.save(buffered, format="PNG")
        # Convert image to base64
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return qr_base64

def generate_unique_qr_code():
# Generate a unique 16-character alphanumeric QR Code, only querying the DB after migration
    qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    # Check if the table exists before querying the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts_restaurant';")
        table_exists = cursor.fetchone() is not None

    if table_exists:
        while Restaurant.objects.filter(qrCodeID=qr_code).exists():
            qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))  # Generate a new one if duplicate

    return qr_code

# Stores Badges
class Badge(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to="badges/")  # Stores badge images in media/badges/

    def __str__(self):
        return self.name

# Tracks the badges a user has earnt
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
    
# Tracks restaurant check in and ensure max 1 check-in per day
class UserCheckIn(models.Model):
    account = models.ForeignKey(account, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    check_in_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('account', 'restaurant', 'check_in_date')  # Ensures only one check-in per day per restaurant

    def __str__(self):
        return f"{self.account.user.username} checked into {self.restaurant.name} on {self.check_in_date}"
