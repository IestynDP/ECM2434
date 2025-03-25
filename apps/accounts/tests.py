from django.test import TestCase
from django.contrib.auth.models import User
from apps.accounts.forms import UserProfileForm
from django.urls import reverse
from apps.accounts.models import account

class UserProfileFormTest(TestCase):
    def test_form(self):
        # Begins test case
        data_for_form = {"first_name": "Iestyn", "last_name": "Perkins", "email": "fk332@test.com", "gdpr_consent": True}
        # Sets up data that will be entered into the user profile form
        user_form = UserProfileForm(data=data_for_form)
        # Emulate the user changing their profile details
        self.assertTrue(user_form.is_valid())
        # The form is true

    def test_form_no_email(self):
        # Begins test case
        data_for_form = {"first_name": "Iestyn", "last_name": "Perkins", "gdpr_consent": True}
        # Sets up data that will be entered into the user profile form
        user_form = UserProfileForm(data=data_for_form)
        # Emulate the user changing their profile details
        self.assertFalse(user_form.is_valid())
        self.assertIn("email", user_form.errors)

    def test_false_gdpr(self):
        # Begins test case
        data_for_form = {"first_name": "Iestyn", "last_name": "Perkins", "email": "fk332@test.com", "gdpr_consent": False}
        # Sets up data that will be entered into the user profile form
        user_form = UserProfileForm(data=data_for_form)
        # Emulate the user changing their profile details
        self.assertFalse(user_form.is_valid())
        self.assertIn("gdpr_consent", user_form.errors)

class RegistrationTest(TestCase):
    def test_registration(self):
        # Begin test
        post = self.client.post(reverse('register'), {'username': 'LongUserName', 'password1': 'UncommonPassword', 'password2': 'UncommonPassword'})
        # This simulates a post request to the URL of the registration view
        self.assertEqual(post.status_code, 302)
        # This assert checks that the post status code is 302, which refers to a page that has had a successful redirection
        self.assertTrue(User.objects.filter(username="LongUserName").exists())
        # This assert checks that the test username has been added to the database and exists

class LoginTest(TestCase):
    def test_user_create(self):
        # Begins test
        User.objects.create_user(username='LongUserName', password='UncommonPassword')
        # Creates a user with a username and a password
        self.assertTrue(User.objects.filter(username="LongUserName").exists())
        # Checks if the user has been created properly and the username credentials are in the database

    def test_user_login(self):
        # Begins test
        User.objects.create_user(username='LongUserName', password='UncommonPassword')
        # Once again creates a user with a username and a password
        logged_in = self.client.login(username='LongUserName', password='UncommonPassword')
        # Emulates an instance in which a user logs in with the same credentials
        post = self.client.get(reverse("home"))
        self.assertEqual(post.status_code, 200)
        # This makes sure that the user has been directed to the home page and that the home page is ready
        self.assertTrue(logged_in, "login failed")
        # Checks the login was true and has an error message for debugging

class ProfilePageTest(TestCase):
    def setUp(self):
        # Begin user set up
        self.user = User.objects.create_user(username='LongUserName', password='UncommonPassword')
        # Creates the user with a username and password
        self.account, created = account.objects.get_or_create(user=self.user, defaults={"points": 100})
        # An account is set up that is associated with the same user and given 100 points for testing
