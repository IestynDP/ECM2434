from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  # Ensure this is imported
from apps.accounts.models import account, Restaurant  # Updated path

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    gdpr_consent = forms.BooleanField(
        required=True,
        label="I agree to the Privacy Policy",
        error_messages={'required': 'You must accept the Privacy Policy to register.'}
    )
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class AccountForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    avatar = forms.ImageField(required=False)

    class Meta:
        model = account
        fields = ["bio", "avatar"]

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "description", "location", "sustainability_features"]