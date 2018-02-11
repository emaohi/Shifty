import json
import logging
from time import sleep

import requests
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime

from django.conf import settings

from core.date_utils import get_next_week_num
from core.models import ShiftSlot
from core.shift_generator import NaiveShiftGenerator
from core.utils import save_holidays
from log.models import Business

logger = logging.getLogger('cool')


@periodic_task(run_every=crontab(minute=0, hour=0))
def get_holidays():

    logger.info("XXXX - In get holidays task")

    year = str(datetime.now().year)
    month = str(settings.HOLIDAY_FETCH_MONTHS)

    holiday_url = 'http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&year=%s&month=%s' % (year, month)

    logger.info('holiday url is %s', holiday_url)

    res = requests.get(holiday_url)

    logger.info('one res is: %s', json.loads(res.text)['items'][0])

    save_holidays(res.text)


@shared_task
def generate_next_week_shifts(business_name):

    sleep(7)

    business = Business.objects.get(pk=business_name)
    next_week = get_next_week_num()
    slots = ShiftSlot.objects.filter(business=business, week=next_week)

    shift_generator = NaiveShiftGenerator(slots)

    shift_generator.generate()

    business.shifts_generated = True
    business.save()

    logger.info('generated shifts for business %s week num %d', business.business_name, next_week)
