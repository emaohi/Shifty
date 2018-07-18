import json
import logging

import requests
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime

from django.conf import settings

from core.date_utils import get_next_week_num
from core.models import ShiftSlot
from core.search import bulk_indexing
from core.shift_generator import ShiftGeneratorFactory
from core.utils import save_holidays
from log.models import Business

logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute=0, hour=0, day_of_week=0))
def get_holidays():

    logger.info("XXXX - In get holidays task")

    year = str(datetime.now().year)
    month = str(settings.HOLIDAY_FETCH_MONTHS)

    holiday_url = 'http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&year=%s&month=%s' % (year, month)

    logger.info('holiday url is %s', holiday_url)

    res = requests.get(holiday_url)

    logger.info('one res is: %s', json.loads(res.text)['items'][0])

    save_holidays(res.text)


@periodic_task(run_every=crontab(minute=0, hour=0, day_of_week=0))
def reset_shift_generation_status():
    logger.info('resetting shift generation statuses for all businesses...')
    for b in Business.objects.all():
        b.reset_shift_generation_status()
        b.save()


@periodic_task(run_every=crontab(minute=0, hour='*/2'))
def index_elastic_search():
    logger.info('Going to index shifts and saved-slots to ES...')
    try:
        err = bulk_indexing()
        if err:
            raise Exception('got errors while indexing: %s', err)
        return 'Indexing to ElasticSearch completed successfully'
    except Exception as e:
        raise Exception('got errors while indexing: %s', e)


@shared_task
def add(x, y):
    return x + y


@shared_task
def generate_next_week_shifts(business_name, level):

    business = Business.objects.get(pk=business_name)
    next_week = get_next_week_num()
    slots = ShiftSlot.objects.filter(business=business, week=next_week)

    shift_generator = ShiftGeneratorFactory.create(level, slots)

    try:
        shift_generator.generate()

        business.set_shift_generation_success()
        business.save()
        logger.info('Generated shifts for business %s week num %d', business.business_name, next_week)

    except Exception as e:
        business.set_shift_generation_failure()
        business.save()
        logger.info('FAILED - generated shifts for business %s week num %d: %s', business.business_name, next_week,
                    str(e))
        raise e
