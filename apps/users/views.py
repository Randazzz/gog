from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from apps.users.forms import UserProfileForm, UserRegistrationForm
from apps.users.models import User


def profile(request):
    user = request.user
    context = {
        'title': 'Профиль',
    }

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if 'remove_avatar' in request.POST:
            user.image.delete()

        if form.is_valid():
            form.save()
            return redirect('users:profile')

    else:
        form = UserProfileForm(instance=user)

    context['form'] = form
    return render(request, 'users/profile.html', context)


def register(request):
    context = {
        'title': 'Регистрация'
    }
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Аккаунт успешно создан!')
        return redirect('users:login')

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
