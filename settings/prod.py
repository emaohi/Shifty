import urlparse

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
CELERY_BROKER_URL = \
    'amqp://d87vKR49:ho9_EJMxh3QTnWyJAdKR4-mHM0ofNF1q@angry-vervain-61.bigwig.lshift.net:10468/h3SbfJQeMSid'

redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'PASSWORD': redis_url.password,
            'DB': 0,
        }
    }
}

RAVEN_CONFIG = {
    'dsn': 'https://95afae5f8bb040c6a70166c7272a10b7:533971d79e4840cfb05b555bcb87f122@sentry.io/286477'
}

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}