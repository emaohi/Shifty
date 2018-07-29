import random

import logging
from abc import ABCMeta, abstractmethod
from django.conf import settings
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Object, Integer, Date, Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import Q

from core.models import Shift

logger = logging.getLogger(__name__)

es_client = connections.create_connection(hosts=[settings.ELASTIC_SEARCH_HOST])


class ShiftIndex(DocType):
    date = Date()
    employees = Object()
    rate = Integer()
    tips = Integer()
    remarks = Text()
    name = Text()

    class Meta:
        index = 'shift'


def bulk_indexing():
    ShiftIndex.init()
    _, shifts_errors = \
        bulk(client=es_client, actions=(b.to_search() for b in Shift.objects.all().iterator()))

    return shifts_errors


class ShiftSearcher:
    def __init__(self, search_strategy):
        self.search_strategy = search_strategy

    def search(self, q, date_from, date_to):
        response = self.search_strategy.search(q, date_from, date_to)
        return [dict(index=hit.meta.index, score=hit.meta.score, body=hit.to_dict(),
                     highlights=hit.meta.highlight.remarks[0]) for hit in response]


class AbstractSearchStrategy:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.es_client = es_client

    @abstractmethod
    def get_query(self, q):
        pass

    def search(self, q, date_from, date_to):
        s = Search(using=self.es_client, ).query(self.get_query(q))\
            .highlight('remarks', pre_tags=['<span style="background-color: #FFFF00">'], post_tags=['</span>'])
        if date_to and date_from:
            s = s.filter('range', date={'gte': date_from, 'lt': date_to,
                                        "format": "yyyy-MM-dd||yyyy"})
        return s.execute()


class PrefixSearchStrategy(AbstractSearchStrategy):
    def __init__(self):
        super(PrefixSearchStrategy, self).__init__()

    def get_query(self, q):
        return Q('match_phrase_prefix', remarks=q)


class MultiMatchSearchStrategy(AbstractSearchStrategy):
    def __init__(self):
        super(MultiMatchSearchStrategy, self).__init__()

    def get_query(self, q):
        return Q("multi_match", query=q, fields=['name', 'remarks'])


def search_strategy_factory():
    chosen = random.choice([PrefixSearchStrategy()])
    logger.debug('chosen strategy: %s', type(chosen))
    return chosen
