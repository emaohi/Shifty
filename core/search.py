from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Boolean, Object
from elasticsearch_dsl.connections import connections

from core.models import SavedSlot

connections.create_connection()


class SavedSlotIndex(DocType):
    name = Text()
    constraints = Object()
    is_mandatory = Boolean()

    class Meta:
        index = 'saved-slot'


def bulk_indexing():
    SavedSlotIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.to_search() for b in SavedSlot.objects.all().iterator()))
