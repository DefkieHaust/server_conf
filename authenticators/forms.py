from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email* (Optional)", min_length=3, max_length=50, required=False)
    insta = forms.CharField(label="Instagram Username", min_length=3, max_length=20)

    class Meta:
        model = User
        fields = ["username", "insta", "email", "password1", "password2"]
