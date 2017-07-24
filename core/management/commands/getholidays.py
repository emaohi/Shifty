from datetime import datetime

import requests
from django.core.management.base import BaseCommand

from core.models import TmpHoliday


class Command(BaseCommand):
    help = 'Fetches holidays information to the database'

    def handle(self, *args, **options):
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        res = requests.get('http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&year=%s&month=%s' %
                           (year, month))
        new_tmp_holiday = TmpHoliday(str(datetime.now()), res.text)
        new_tmp_holiday.save()
