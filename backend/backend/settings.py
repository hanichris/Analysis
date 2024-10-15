"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import ssl
import sys
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY_NEW')
SECRET_KEY_FALLBACKS = [os.getenv('SECERET_KEY_OLD')]

if SECRET_KEY is None:
    raise RuntimeError('Could not find a secret key in the environment.')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost:127.0.0.1').split(':')

# Custom user model to use
AUTH_USER_MODEL = "analysis.User"


# Application definition

INSTALLED_APPS = [
    'daphne',
    'analysis.apps.AnalysisConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bleach',
    'rest_framework',
    'phonenumber_field',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': 5432,
        'OPTIONS': {
            'pool': True,
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    pass
else:
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'


STATIC_URL = 'static/'
STATIC_ROOT = '/var/www/divergentspace/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Login redirect url
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'analysis:dashboard'
LOGOUT_REDIRECT_URL = 'analysis:index'

# CSRF settings
CSRF_TRUSTED_ORIGINS = ['https://previously-funny-bee.ngrok-free.app', 'https://*.divergentspace.com']
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

# HSTS Configuration
SECURE_HSTS_SECONDS = 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

SESSION_COOKIE_SECURE = True


# Bleach Configuration
# Allowed HTML tags
BLEACH_ALLOWED_TAGS = ['p', 'strong', 'ul', 'li']

# Strip unknown tags if True, replace with HTML escaped characters if False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False


# Celery Configuration
CELERY_BROKER_URL = os.getenv("RABBITMQ_URL")
CELERY_ACCEPT_CONTENT = {'json'}
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_USE_SSL = {
    'ca_certs': '/etc/ssl/certs/Amazon_Root_CA_4.pem',
    'cert_reqs': ssl.CERT_REQUIRED,
}
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'eu-north-1',
    'queue_name_prefix': 'dspacermq',
    'visibility_timeout': 1800000,
    'polling_interval': 10,
    'is_safe': True,
    'max_retries': 5,
}

# Cache Configuration
#CACHES = {
#    "default": {
#        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
#        "LOCATION": "dspacememcache.ogiqmr.0001.eun1.cache.amazonaws.com:11211",
#    }
#}

# SITE ID FOR USE WITH THE SITES FRAMEWORK
SITE_ID = 1

# EMAIL CONFIGURATION
# RESEND_SMTP_PORT = 587
# RESEND_SMTP_USERNAME = 'resend'
# RESEND_SMTP_HOST = 'smtp.resend.com'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
