from django.contrib import admin

from apps.users.models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_verified_email')
    fields = (
        ('username', 'first_name'),
        ('email', 'is_verified_email'),
        'password',
        'image',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined',
        'groups',
        'user_permissions',
    )
    search_fields = ('username',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'expires_at', 'code')
    fields = ('user', 'expires_at', 'created_at', 'code')
    readonly_fields = ('created_at',)
