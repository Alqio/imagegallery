"""
Django settings for imagegallery project.

Generated by 'django-admin startproject' using Django 1.11.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url

# from .storage_backends import MediaStorage
# import storages.backends

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "true"
PRODUCTION = os.environ.get("PRODUCTION") == "true"

print(f"Debug: {DEBUG}, Production: {PRODUCTION}")

ALLOWED_HOSTS = [
    'localhost',
    'alqio.com',
    'www.alqio.com',
    'saarangalleria.net',
    'www.saarangalleria.net'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'images.apps.ImagesConfig',
    'imagegallery.apps.ImagegalleryConfig',
    'api.apps.ApiConfig',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'imagegallery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'imagegallery.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECURE_SSL_REDIRECT = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

"""
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static')
)
"""

if PRODUCTION:
    # django-storages setup for AWS
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET')

    AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com'

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400'
    }

    AWS_S3_SIGNATURE_VERSION = 's3v4'

    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'

    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
