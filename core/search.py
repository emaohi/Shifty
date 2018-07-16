from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Boolean, Object, Integer, Date, Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MultiMatch

from core.models import SavedSlot, Shift

connections.create_connection()


class SavedSlotIndex(DocType):
    name = Text()
    constraints = Object()
    is_mandatory = Boolean()

    class Meta:
        index = 'saved-slot'


class ShiftIndex(DocType):
    date = Date()
    employees = Object()
    rate = Integer()
    tips = Integer()
    remarks = Text()

    class Meta:
        index = 'shift'


def bulk_indexing():
    SavedSlotIndex.init()
    ShiftIndex.init()
    es = Elasticsearch()
    saved_slots_success, saved_slots_errors = \
        bulk(client=es, actions=(b.to_search() for b in SavedSlot.objects.all().iterator()))
    shifts_success, shifts_errors = \
        bulk(client=es, actions=(b.to_search() for b in Shift.objects.all().iterator()))

    return saved_slots_errors + shifts_errors


def search_term(q):
    client = Elasticsearch()

    s = Search(using=client,) \
        .query(MultiMatch(query=q))
    response = s.execute()

    for hit in response:
        return dict(index=hit.meta.index, score=hit.meta.score, body=hit.to_dict())
