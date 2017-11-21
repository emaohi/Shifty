from base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shifty',
        'USER': 'root',
        'PASSWORD': 'Lucky123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CELERY = True
CELERY_BROKER_URL = 'pyamqp://guest@localhost//'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': "redis://127.0.0.1:6379/1",
    },
}