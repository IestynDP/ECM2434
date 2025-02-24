from django.shortcuts import render
from .models import Category, Question, Answer
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import account  # Import the account model


def home(request: HttpRequest) -> HttpResponse:
    """Renders the quiz home page, listing all quiz categories"""
    categories = Category.objects.all()
    return render(request, 'quiz_home.html', {'categories': categories})


def quiz(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category)
    return render(request, 'quiz.html',
                  {'category': category, 'questions': questions})


@login_required
def submit_quiz(request, category_id):
    if request.method == 'POST':
        correct_answers = 0
        total_questions = 0
        for question in Question.objects.filter(category_id=category_id):
            total_questions += 1
            selected_answer = request.POST.get(str(question.id))
            if selected_answer:
                answer = Answer.objects.get(id=selected_answer)
                if answer.is_correct:
                    correct_answers += 1
        if total_questions:
            score = (correct_answers / total_questions) * 100
        else:
            score = 0

        if score >= 90:
            rank = "Well done! You are a genius!"
        elif score < 20:
            rank = "Ohh, try again!"
        else:
            rank = "Not bad! Keep it up!"

        # Update user's points
        user_account, created = account.objects.get_or_create(user=request.user)
        user_account.points += 1
        user_account.save()

        context = {
            'score': score,
            'rank': rank
        }
    return render(request, 'result.html', context)
