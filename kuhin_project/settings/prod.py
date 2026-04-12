"""
Django settings for kuhin_project — PRODUCTION

This file contains production-specific settings.
Uses PostgreSQL, HTTPS, and Cloudinary for media storage.
"""

from .base import *
import environ
import os

env = environ.Env()

# SECURITY: Load from environment variables
SECRET_KEY = env('SECRET_KEY')

DEBUG = False

# Only allow specific hosts in production
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['yourdomain.com', 'www.yourdomain.com'])

# Database — PostgreSQL for production
DATABASES = {
    'default': env.db('DATABASE_URL')  # Expects: postgres://user:pass@host:port/dbname
}

# Email — SMTP for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# ==============================================================================
# SSL/HTTPS SECURITY
# ==============================================================================
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# XSS and Frame protection
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "cdn.jsdelivr.net", "code.jquery.com", "cdnjs.cloudflare.com"),
    'style-src': ("'self'", "cdn.jsdelivr.net", "fonts.googleapis.com", "cdnjs.cloudflare.com"),
    'font-src': ("'self'", "fonts.gstatic.com", "cdnjs.cloudflare.com"),
    'img-src': ("'self'", "data:", "res.cloudinary.com"),
    'frame-src': ("'self'",),
}

# ==============================================================================
# CDN & STATIC FILES
# ==============================================================================
# Cloudinary for media uploads (images, documents)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary credentials from environment
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

# Static files are served by WhiteNoise (configured in base.py)
# They're cached for 1 year at the CDN level
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# CACHING
# ==============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'health_check_interval': 30},
        },
        'KEY_PREFIX': 'kuhin',
        'TIMEOUT': 300,
    }
}

# Session caching
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# ==============================================================================
# LOGGING
# ==============================================================================
# Sentry for error tracking (optional)
if env('SENTRY_DSN', default=''):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True,
    )

# File and console logging for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'kuhin_production.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# ==============================================================================
# ALLOWED HOSTS VALIDATION
# ==============================================================================
# Fail if ALLOWED_HOSTS is not configured
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['yourdomain.com', 'www.yourdomain.com']:
    raise ValueError(
        "ALLOWED_HOSTS must be set in .env for production. "
        "Example: ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com"
    )
