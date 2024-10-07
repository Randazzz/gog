from django.urls import path
from django.contrib.auth.views import LogoutView

from apps.users.views import profile, register, login_view

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='registration'),

]
