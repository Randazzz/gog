from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.template import context

from apps.users.forms import UserRegistrationForm


def profile(request):
    return render(request, 'users/profile.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан!')
            return redirect('users:login')
        else:
            return render(request, 'users/register.html', {"form": form})
    else:
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {"form": form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:

            messages.error(request, 'Неверное имя пользователя или пароль.')
            return render(request, 'users/login.html')
    else:
        has_success = {'has_success': messages.get_messages(request)}
        return render(request, 'users/login.html', context=has_success)
