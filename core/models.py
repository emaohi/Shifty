from __future__ import unicode_literals

from django.db import models

from log.models import Business


class ShiftsArrangement(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    # Json in the structure of:
    # {sunday:[{start:<>, end:<>}, {}, {}...]}, monday: [], ..., saturday:[]}
    arrangement = models.TextField(max_length=200)
    submit_deadline = models.DateTimeField()
