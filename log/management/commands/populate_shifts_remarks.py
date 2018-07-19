import json
import logging
from time import time

import requests
from django.core.management import BaseCommand

from core.models import Shift

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    quotes_url = 'http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1'

    help = 'populate shifts remarks with random quotes'

    # # pylint: disable=broad-except
    def handle(self, *args, **options):
        try:
            start_time = time()
            self._populate_remarks()
            end_time = time()
            logger.info('population took: %s seconds', end_time - start_time)
        except Exception as e:
            logger.error('remarks population failed %s', e.message)

    def _populate_remarks(self):
        for shift in Shift.objects.all():
            quote = self._fetch_random_quote()
            shift.remarks = quote
            logger.info('putting %s to shift %s', quote, shift)
            shift.save()

    def _fetch_random_quote(self):
        raw_quote = json.loads(requests.get(self.quotes_url).content)[0]['content']
        return raw_quote.strip("<p>").replace("</p>\n", "")
