from django.conf import settings
from django.contrib.auth.views import (LoginView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.users.forms import (UserLoginForm, UserProfileForm,
                              UserRegistrationForm)
from apps.users.models import EmailVerification, User
from apps.users.tasks import send_email_verification


class UserProfileView(UpdateView):
    extra_context = {'title': 'Профиль'}
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if 'remove_avatar' in request.POST:
            user.image.delete()
        if 'resend_email' in request.POST and not user.is_verified_email:
            EmailVerification.objects.filter(user=user).delete()
            send_email_verification.delay(user.id)
        return super().post(request, *args, **kwargs)


class UserRegistrationView(SuccessMessageMixin, CreateView):
    extra_context = {'title': 'Регистрация'}
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'
    success_message = 'Вы успешно зарегистрировались! На вашу эл. почту отправлено письмо с подтверждением.'


class UserLoginView(LoginView):
    extra_context = {'title': 'Авторизация'}
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class EmailVerificationView(TemplateView):
    extra_context = {'title': 'Подтверждение эл. почты'}
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(self, request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('index'))


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')
    extra_email_context = {'domain': settings.DOMAIN_NAME, 'site_name': 'Grace of the Gods'}

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            return super().form_valid(form)
        else:
            form.add_error('email', 'Пользователь с таким адресом электронной почты не найден.')
            return self.form_invalid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
