from django import forms
from django.contrib.auth.models import User
from .models import account

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class AccountForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    avatar = forms.ImageField(required=False)

    class Meta:
        model = account
        fields = ["bio", "avatar"]
