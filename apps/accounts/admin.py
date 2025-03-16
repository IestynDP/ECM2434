from django.contrib import admin
from .models import account, tasks, Restaurant
from apps.quiz.models import Category, Question, Answer  # Updated path

admin.site.register(account)
admin.site.register(Restaurant)
admin.site.register(tasks)
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)