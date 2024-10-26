from django.contrib import admin

from apps.users.models import User


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
