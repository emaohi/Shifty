import requests
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime

from django.conf import settings
from core.utils import save_holidays


@periodic_task(run_every=crontab(0, 0, day_of_month='2'))
def get_holidays():

    year = str(datetime.now().year)
    month = str(settings.HOLIDAY_FETCH_MONTHS)

    res = requests.get('http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&year=%s&month=%s' %
                       (year, month))

    save_holidays(res.text)
