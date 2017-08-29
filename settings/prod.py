from base import *

DEBUG = True

ALLOWED_HOSTS = ['shifty-app.herokuapp.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_ab2a741886e22c8',
        'USER': 'b0b83db77ed36d',
        'PASSWORD': 'dbe5049c',
        'HOST': 'us-cdbr-iron-east-05.cleardb.net',
        'PORT': '3306',
    }
}

CELERY = True
CELERY_BROKER_URL =\
    'amqp://d87vKR49:ho9_EJMxh3QTnWyJAdKR4-mHM0ofNF1q@angry-vervain-61.bigwig.lshift.net:10468/h3SbfJQeMSid'
