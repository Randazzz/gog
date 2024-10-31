from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from apps.products.models import Basket
from apps.users.forms import UserProfileForm, UserRegistrationForm, UserLoginForm
from apps.users.models import User


class UserProfileView(UpdateView):
    extra_context = {'title': 'Профиль'}
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if 'remove_avatar' in request.POST:
            user.image.delete()
        return super().post(request, *args, **kwargs)


class UserRegistrationView(SuccessMessageMixin, CreateView):
    extra_context = {'title': 'Регистрация'}
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'
    success_message = 'Вы успешно зарегистрировались!'


class UserLoginView(LoginView):
    extra_context = {'title': 'Авторизация'}
    template_name = 'users/login.html'
    form_class = UserLoginForm


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#
#             messages.error(request, 'Неверное имя пользователя или пароль.')
#             return render(request, 'users/login.html')
#     else:
#         context = {'has_success': messages.get_messages(request)}
#         return render(request, 'users/login.html', context)
