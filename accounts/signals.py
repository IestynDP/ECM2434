from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import account

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    """Automatically create an account instance when a User is created."""
    if created:
        account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    """Save the account when the User is saved."""
    instance.account.save()
