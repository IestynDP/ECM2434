from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Question, Answer, UserQuizScore
from apps.accounts.models import account, UserBadge, Badge

class QuizTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        # Logs in the test user

        # Create test category
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        # Sets up a test category

        # Create test questions and answers
        self.question1 = Question.objects.create(category=self.category, text='Test Question 1')
        self.answer1_1 = Answer.objects.create(question=self.question1, text='Answer 1', is_correct=True)
        self.answer1_2 = Answer.objects.create(question=self.question1, text='Answer 2', is_correct=False)
        # Sets up the first test question with answers

        self.question2 = Question.objects.create(category=self.category, text='Test Question 2')
        self.answer2_1 = Answer.objects.create(question=self.question2, text='Answer 1', is_correct=False)
        self.answer2_2 = Answer.objects.create(question=self.question2, text='Answer 2', is_correct=True)
        # Sets up the second test question with answers

        # Check for existing account and create if necessary
        self.user_account, created = account.objects.get_or_create(user=self.user, defaults={'points': 0, 'total_points': 0})
        # Ensures the user has an associated account with default points

    def test_home_view(self):
        response = self.client.get(reverse('quiz_home'))
        self.assertEqual(response.status_code, 200)
        # Checks that the home view is accessible
        self.assertContains(response, 'Test Category')
        # Verifies that the test category is displayed on the home view

    def test_quiz_view(self):
        response = self.client.get(reverse('quiz', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        # Checks that the quiz view is accessible
        self.assertContains(response, 'Test Question 1')
        self.assertContains(response, 'Test Question 2')
        # Verifies that the test questions are displayed on the quiz view

    def test_submit_quiz_view(self):
        # Manually set user's total points to 95
        self.user_account.total_points = 95
        self.user_account.save()
        # Updates the user's total points for testing

        response = self.client.post(reverse('submit_quiz', args=[self.category.id]), {
            str(self.question1.id): self.answer1_1.id,
            str(self.question2.id): self.answer2_2.id,
        })
        self.assertEqual(response.status_code, 200)
        # Checks that the quiz submission view is accessible
        self.assertContains(response, 'Well done! You are a genius!')
        # Verifies that the success message is displayed

        # Check user points and highest score
        user_quiz_score = UserQuizScore.objects.get(user=self.user, category=self.category)
        self.assertEqual(user_quiz_score.highest_score, 100)
        # Verifies that the user's highest score is updated correctly
        self.user_account.refresh_from_db()
        self.assertEqual(self.user_account.points, 5)
        self.assertEqual(self.user_account.total_points, 100)
        # Verifies that the user's points and total points are updated correctly

        # Check badges
        self.assertTrue(UserBadge.objects.filter(user=self.user, badge__name='Point Collector').exists())
        # Verifies that the user has earned the 'Point Collector' badge