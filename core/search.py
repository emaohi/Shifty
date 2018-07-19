from django.conf import settings
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Object, Integer, Date, Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MatchPhrasePrefix

from core.models import Shift

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


def search_term(q):

    s = Search(using=es_client,) \
        .query(MatchPhrasePrefix(remarks={"query": q}))
    response = s.execute()

    return [dict(index=hit.meta.index, score=hit.meta.score, body=hit.to_dict()) for hit in response]
