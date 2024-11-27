from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.users.views import (EmailVerificationView, UserLoginView,
                              UserProfileView, UserRegistrationView,
                              CustomPasswordResetView, CustomPasswordResetConfirmView,
                              CustomPasswordResetDoneView, CustomPasswordResetCompleteView)

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
