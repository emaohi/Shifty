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
