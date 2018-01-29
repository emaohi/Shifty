import json
import logging
import requests
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime

from django.conf import settings
from core.utils import save_holidays

logger = logging.getLogger('cool')


@periodic_task(run_every=crontab())
def get_holidays():

    logger.info("XXXX - In get holidays task")

    year = str(datetime.now().year)
    month = str(settings.HOLIDAY_FETCH_MONTHS)

    holiday_url = 'http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&year=%s&month=%s' % (year, month)

    logger.info('holiday url is %s', holiday_url)

    res = requests.get(holiday_url)

    logger.info('one res is: %s', json.loads(res.text)['items'][0])

    save_holidays(res.text)
