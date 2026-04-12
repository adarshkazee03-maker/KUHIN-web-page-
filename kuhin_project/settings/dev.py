"""
Django settings for kuhin_project — DEVELOPMENT

This file contains development-specific settings.
Uses a local SQLite database and console email backend.
"""

from .base import *
import environ

env = environ.Env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-h=-7+dcc$zylm0rf06&2oqdp+-%vk$7p9ba-5&m^k$6w)po373')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

# Database — SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email — Console backend for development (prints to stdout)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files — no compression in dev
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Security settings disabled in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Allow all origins for CORS in development (if using CORS)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Use local media storage in development
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
