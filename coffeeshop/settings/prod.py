from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "yourdomain.com",
    "www.yourdomain.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "coffee_shop",
        "USER": "coffee_user",
        "PASSWORD": "strong-password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
