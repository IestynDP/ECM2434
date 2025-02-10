from django.contrib import admin
from .models import account, tasks

admin.site.register(account)
admin.site.register(tasks)