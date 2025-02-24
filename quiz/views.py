from django.shortcuts import render
from .models import Category, Question, Answer

def home(request):
    categories = Category.objects.all()
    return render(request, 'quiz_home.html', {'categories': categories})

def quiz(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category)
    return render(request, 'quiz.html', {'category': category, 'questions': questions})

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
        score = (correct_answers / total_questions) * 100 if total_questions else 0
        return render(request, 'result.html', {'score': score})
