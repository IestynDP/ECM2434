from django.shortcuts import render, get_object_or_404
from .models import Category, Question, Answer, UserQuizScore
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from apps.accounts.models import account, UserBadge, Badge  # Updated path
from django.contrib import messages
from django.contrib.messages import get_messages





def home(request: HttpRequest) -> HttpResponse:
    """Renders the quiz home page, listing all quiz categories"""
    categories = Category.objects.all()
    return render(request, 'quiz_home.html', {'categories': categories})

@login_required
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
            points = 5
        elif score >= 70:
            rank = "Great job!"
            points = 4
        elif score >= 50:
            rank = "Good effort!"
            points = 3
        elif score >= 30:
            rank = "Keep trying!"
            points = 2
        elif score >= 10:
            rank = "Needs improvement!"
            points = 1
        else:
            rank = "Ohh, try again!"
            points = 0

        # Update user's points based on improved performance
        user_account = get_object_or_404(account, user=request.user)
        user_quiz_score, created = UserQuizScore.objects.get_or_create(user=request.user, category_id=category_id)
        if score > user_quiz_score.highest_score:
            additional_points = points - user_quiz_score.highest_score // 20
            user_account.points += additional_points
            user_account.save()
            user_quiz_score.highest_score = score
            user_quiz_score.save()

        # Award "Quiz Master" Badge if score is 100%
        if score == 100:
            quiz_badge, created = Badge.objects.get_or_create(name="Quiz Master", defaults={
                "description": "Awarded for scoring 100% on a quiz.",
                "icon": "badges/quiz_master.png"
            })

            if not UserBadge.objects.filter(user=request.user, badge=quiz_badge).exists():
                UserBadge.objects.create(user=request.user, badge=quiz_badge)
                messages.success(request, "Congratulations! You've earned the 'Quiz Master' badge!")

        storage = get_messages(request)
        for _ in storage:
            pass  # consumes messages, preventing duplication

    context = {
        'score': score,
        'rank': rank
    }
    return render(request, 'result.html', context)
