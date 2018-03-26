import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = ['emaohi@gmail.com']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=uk5_$pry_5=k(8g5&-$=(&^4=8320(n4&80!01xnbnb&*)1*7'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'raven.contrib.django.raven_compat',
    'log',
    'core',
    'menu'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Shifty.urls'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'Shifty.wsgi.application'

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

LOGIN_REDIRECT_URL = '/login_success'  # It means home view
LOGIN_URL = '/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jerusalem'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# Email settings

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'shifty.moti'

EMAIL_HOST_PASSWORD = 'Lucky123'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s line num:%(lineno)s msg:[%(message)s]'
        },
        'regular': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console-regular-info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'regular'
        },
        'console-verbose': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        }
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console-verbose', 'sentry'],
        },
        'log': {
            'level': 'INFO',
            'handlers': ['console-verbose', 'sentry'],
            'propagate': False,
        },
        'core': {
            'level': 'INFO',
            'handlers': ['console-verbose', 'sentry'],
            'propagate': False,
        },
        'menu': {
            'level': 'INFO',
            'handlers': ['console-verbose', 'sentry'],
            'propagate': False,
        }
    },
}

HOLIDAY_FETCH_MONTHS = 'all'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_MAIL_TIMEOUT = 45000
CELERY_HIJACK_ROOT_LOGGER = False

# Google APIs
DISTANCE_API_KEY = 'AIzaSyBuVvbfu_0nMgFmagXaWdIsVyXrL41OV-U'
DISTANCE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=%s&key=%s'
DIRECTIONS_URL = 'https://maps.google.com/maps/dir/?api=1&origin=%s&destination=%s&travelmode=%s'

# profanity filter
PROFANITY_SERVICE_URL = 'http://www.purgomalum.com/service/containsprofanity?text=%s'

# restaurant logo lookup url
LOGO_LOOKUP_URL = 'https://www.rest.co.il/restaurants/israel/?kw=%s'

RAVEN_CONFIG = {}

DURATION_CACHE_TTL = 15 * 60

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

USE_TOOLBAR = False
