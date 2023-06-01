from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
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


class PasswordRecoveryForm(forms.Form):
    username = forms.CharField()
    totp_code = forms.IntegerField()


class CustomPasswordResetForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid username')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data