import requests
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime

from core.models import TmpHoliday


@periodic_task(run_every=crontab())
def get_holidays():
    res = requests.get('http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&year=2017&month=9')
    new_tmp_holiday = TmpHoliday(str(datetime.now()), res.text)
    new_tmp_holiday.save()
