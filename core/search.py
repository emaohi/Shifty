from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Boolean, Object, Integer, Date
from elasticsearch_dsl.connections import connections

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
    bulk(client=es, actions=(b.to_search() for b in SavedSlot.objects.all().iterator()))
    bulk(client=es, actions=(b.to_search() for b in Shift.objects.all().iterator()))
