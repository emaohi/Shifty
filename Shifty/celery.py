from __future__ import absolute_import, unicode_literals

import logging
import os
from celery import Celery
from celery.signals import after_setup_task_logger
from celery.signals import after_setup_logger
import logstash

# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

app = Celery(str('Shifty'))

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


def initialize_logstash(logger=None, loglevel=logging.INFO, **kwargs):
    handler = logstash.TCPLogstashHandler('localhost', 5959, tags=['celery'], message_type='celery', version=1)
    handler.setLevel(loglevel)
    logger.addHandler(handler)
    return logger


if settings.LOGSTASH:
    after_setup_task_logger.connect(initialize_logstash)
    after_setup_logger.connect(initialize_logstash)
