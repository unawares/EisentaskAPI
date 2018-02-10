from .base import *
from .utils.stream import SettingsFile

# Debug

DEBUG = True


settings = SettingsFile('../eisentask_config_dev.json')


# Allowed hosts

ALLOWED_HOSTS = ['192.168.43.29', 'localhost',]


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': settings.get_env_var("DB_NAME"),
        'USER': settings.get_env_var("DB_USER"),
        'PASSWORD': settings.get_env_var("DB_PASS"),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Email

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = settings.get_env_var("EMAIL_USER")
EMAIL_HOST_PASSWORD = settings.get_env_var("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
