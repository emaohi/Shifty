from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Object, Integer, Date, Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MatchPhrasePrefix

from core.models import Shift

connections.create_connection()


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
    es = Elasticsearch()
    _, shifts_errors = \
        bulk(client=es, actions=(b.to_search() for b in Shift.objects.all().iterator()))

    return shifts_errors


def search_term(q):
    client = Elasticsearch()

    s = Search(using=client,) \
        .query(MatchPhrasePrefix(remarks={"query": q}))
    response = s.execute()

    return [dict(index=hit.meta.index, score=hit.meta.score, body=hit.to_dict()) for hit in response]
