"""
Development settings for SaberAngola project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable caching in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Development-specific logging
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['saberangola']['level'] = 'DEBUG'

# Development CORS settings
CORS_ALLOW_ALL_ORIGINS = True