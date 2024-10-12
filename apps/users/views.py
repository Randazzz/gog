from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from apps.users.forms import UserRegistrationForm


def profile(request):
    context = {
        'title': 'Профиль'
    }
    return render(request, 'users/profile.html', context)


def register(request):
    context = {
        'title': 'Регистрация'
    }
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан!')
            return redirect('users:login')
        else:
            context['form'] = form
            return render(request, 'users/register.html', context)
    else:
        form = UserRegistrationForm()
        context['form'] = form
        return render(request, 'users/register.html', context)


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
        context = {'has_success': messages.get_messages(request)}
        return render(request, 'users/login.html', context)
