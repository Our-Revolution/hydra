from django.contrib import messages
import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = '*'


# Application definition

INSTALLED_APPS = [
    
    # core Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # dev niceties
    'anymail',
    'bootstrap3',
    'cacheops',
    'debug_toolbar',
    'espresso',
    
    # Hydra specific
    'bsd',
    'hydra',
]


# Mailgun


MAILGUN_ACCESS_KEY = os.environ.get('MAILGUN_API_KEY', None)
MAILGUN_SERVER_NAME = os.environ.get('MAILGUN_API_DOMAIN', None)
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)


ANYMAIL = {
    'MAILGUN_API_KEY': MAILGUN_ACCESS_KEY,
    'MAILGUN_SENDER_DOMAIN': MAILGUN_SERVER_NAME
}

DEFAULT_FROM_EMAIL = "organizing@ourrevolution.com"


# espresso settings

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

else:
    EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'anymail.backends.mailgun.MailgunBackend')


DRIP_TEMPLATES = (
    (None, 'None'),
    ('our_revolution_email.html', 'Our Revolution'),
)


# debug / email reporting settings

ADMINS = [('Jon', 'jon@ourrevolution.com'), ('Chris', 'chris@ourrevolution.com')]

SERVER_EMAIL = "bugtroll@ourrevolution.com"

INTERNAL_IPS = ['24.18.176.26', '24.158.161.75']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'hydra.settings.LOAD_BALANCER_FRIENDLY_SHOW_TOOLBAR'    
}


DEBUG_TOOLBAR_PANELS = [
    # 'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


def LOAD_BALANCER_FRIENDLY_SHOW_TOOLBAR(request):
    
    if request.META.get('REMOTE_ADDR', None) not in INTERNAL_IPS and request.META.get('HTTP_X_FORWARDED_FOR', None) not in INTERNAL_IPS:
        return False

    if request.is_ajax():
        return False

    return bool(DEBUG)



MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
            'builtins': [
                'espresso.templatetags.clean_spaces'
            ]
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
        'ENGINE': "bsd.mysql",  # hack.
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

LOGIN_URL = '/login/'
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

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


CACHEOPS_REDIS = { 'host': os.environ.get('REDIS_HOST', None), 'db': 1 }

CACHEOPS = {
    'bsd.EventType': {'ops': ('fetch',), 'timeout': 60*60},
    'bsd.Constituent': {'ops': ('get', 'fetch'), 'timeout': 60*60},
    # 'bsd.Event': {'ops': ('all,'), 'timeout': 10, 'cache_on_save': True}
}

CACHEOPS_DEGRADE_ON_FAILURE = True


if not DEBUG:
    MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS.remove('debug_toolbar')