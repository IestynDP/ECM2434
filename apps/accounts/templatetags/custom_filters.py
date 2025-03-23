from django import template
from apps.accounts.models import account  # If you are using Account for avatars

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_avatar(user):
    try:
        return user.account.avatar.url if user.account and user.account.avatar else None
    except account.DoesNotExist:
        return None