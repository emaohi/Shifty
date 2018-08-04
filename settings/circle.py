from base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'circle_test',
        'USER': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

CELERY = True
CELERY_BROKER_URL = 'pyamqp://guest@localhost//'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}