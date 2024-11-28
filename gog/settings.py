"""
Django settings for gog project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

from django.contrib import messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sw!a-wl=sueygs#lg$qpa-8yzi9uou%f!65333$!f=a@e-xu(m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DOMAIN_NAME = 'http://127.0.0.1:8000'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    'allauth.socialaccount',
    'allauth',
    'allauth.account',
    'allauth.socialaccount.providers.github',
    'debug_toolbar',

    'apps.products',
    'apps.users',
    'apps.orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'gog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.products.context_processors.baskets'
            ],
        },
    },
]

WSGI_APPLICATION = 'gog.wsgi.application'

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gog_db',
        'USER': 'gog_username',
        'PASSWORD': 'gog_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Users
LOGOUT_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Verification email
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'graceof.thegods@yandex.ru'
EMAIL_HOST_PASSWORD = 'qzcelyomjfpvqgjb'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'graceof.thegods@yandex.ru'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# OAuth

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

SOCIALACCOUNT_QUERY_EMAIL = True

SOCIALACCOUNT_ADAPTER = 'apps.users.allauth_adapter.SocialAccountAdapter'

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "VERIFIED_EMAIL": True,
        'SCOPE': [
            'user',
            'user:email',
        ],
        'EMAIL_AUTHENTICATION': True,
    },
}

# Celery

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'

# Stripe

STRIPE_PUBLIC_KEY = 'pk_test_51Pq9gtFEYi1z8K65wTPojg4vgJe2ZzxWcrVYonv2AIjnQWXcxd0LVt1Zo57yWylpvF0njxxbXIF8j795YmTEYxk900mvbhKNPY'
STRIPE_SECRET_KEY = 'sk_test_51Pq9gtFEYi1z8K65GCAX2jQONq7Nenmxisdl0MF6FkYkBA5XS5y4YebdawHUwZH0FR72pQEkloBYYZAExiOJXmLQ00zANQ7joE'
STRIPE_WEBHOOK_SECRET = 'whsec_629f9cde35ed384f693c2905cd6ed9a25e8cea640c5623ee933fcb3e85033f7d'
