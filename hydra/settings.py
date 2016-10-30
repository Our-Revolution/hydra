"""
Django settings for hydra project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'bootstrap3',
    
    'bsd',
    'hydra',
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

ROOT_URLCONF = 'hydra.urls'

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

WSGI_APPLICATION = 'hydra.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

BSD_API_HOST    = os.environ.get('BSD_API_HOST')
BSD_API_ID      = os.environ.get('BSD_API_ID')
BSD_API_SECRET  = os.environ.get('BSD_API_SECRET')

DATABASES = {

    # Postgres / default
    'default': dj_database_url.config(),

    # Blue State Digital read-only replica, for majortom
    'BSD': {
        'ENGINE': "django.contrib.gis.db.backends.mysql",
        'NAME': os.environ.get('BSD_DATABASE_NAME'),
        'USER': os.environ.get('BSD_DATABASE_USER'),
        'HOST': os.environ.get('BSD_DATABASE_HOST'),
        'PASSWORD': os.environ.get('BSD_DATABASE_PASSWORD'),
        'OPTIONS': {
            'ssl': {
                'ca': os.path.join(BASE_DIR, os.environ.get('BSD_DATABASE_PATH_TO_CA_CERT')),
                'cipher': "DHE-RSA-AES256-SHA",
                'verify_server_cert': False
            }
        }
    }

}


DATABASE_ROUTERS = ['bsd.routers.BSDRouter']

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'bsd.backends.BSDAuthenticationBackend',)

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '.static')


# Mailgun

MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
MAILGUN_API_DOMAIN = os.environ.get('MAILGUN_API_DOMAIN', None)
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)
