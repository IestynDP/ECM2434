from django.contrib import admin
from .models import account, tasks, Restaurant,items,purchases
from apps.quiz.models import Category, Question, Answer  # Updated path

admin.site.register(account)
admin.site.register(Restaurant)
admin.site.register(tasks)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(items)
admin.site.register(purchases)