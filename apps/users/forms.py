from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, label='Имя пользователя', widget=forms.TextInput())
    email = forms.EmailField(required=True, label='Электронная почта', widget=forms.TextInput())
    password1 = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label='Подтверждение пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
