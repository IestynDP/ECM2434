from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='quiz_home'),
    path('quiz/<int:category_id>/', views.quiz, name='quiz'),
    path('submit_quiz/<int:category_id>/', views.submit_quiz, name='submit_quiz'),
]
