from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User
from .models import Address


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email* (Optional)", min_length=3, max_length=50, required=False)
    insta = forms.CharField(label="Instagram Username", min_length=3, max_length=20)

    class Meta:
        model = User
        fields = ["username", "insta", "email", "password1", "password2"]

class UpdateForm(UserChangeForm):
    email = forms.EmailField(label="Email* (Optional)", min_length=3, max_length=50, required=False)
    insta = forms.CharField(label="Instagram Username", min_length=3, max_length=20)
    password = None

    class Meta:
        model = get_user_model()
        fields = ["username", "insta", "email"]


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ("name", "street", "city", "postcode")
