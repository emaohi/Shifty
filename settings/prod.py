import urlparse

from base import *

DEBUG = True

ALLOWED_HOSTS = ['shifty-app.herokuapp.com']

ELASTIC_SEARCH_HOST = 'https://4x6a0d8d5b:f35zpwauc2@redwood-3158069.us-east-1.bonsaisearch.net'

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
CELERY_BROKER_URL = urlparse.urlparse(os.environ.get('CLOUDAMQP_URL'))

redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'PASSWORD': redis_url.password,
            'DB': 0,
        }
    }
}

RAVEN_CONFIG = {
    'dsn': 'https://95afae5f8bb040c6a70166c7272a10b7:533971d79e4840cfb05b555bcb87f122@sentry.io/286477'
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
