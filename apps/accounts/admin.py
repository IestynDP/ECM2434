from django.contrib import admin
<<<<<<< HEAD:accounts/admin.py
from .models import account, tasks, Restaurant
from quiz.models import Category, Question, Answer
=======
from .models import account, tasks
from apps.quiz.models import Category, Question, Answer  # Updated path
>>>>>>> 1505391f9afbe37ab43d6719c9308aeab2dfdce5:apps/accounts/admin.py

admin.site.register(account)
admin.site.register(tasks)
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)