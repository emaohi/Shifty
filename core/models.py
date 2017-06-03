from __future__ import unicode_literals

from django.db import models

from log.models import Business, EmployeeProfile


class ShiftsArrangement(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    # Json in the structure of:
    # {sunday:[{start:<>, end:<>}, {}, {}...]}, monday: [], ..., saturday:[]}
    arrangement = models.TextField(max_length=200)
    submit_deadline = models.DateTimeField()


class Message(models.Model):
    sender = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='msg_send')
    recipients = models.ManyToManyField(EmployeeProfile, related_name='msg_receive')
    sent_time = models.DateTimeField()
    subject = models.TextField(max_length=50)
    text = models.TextField(max_length=200)

    def get_recipients(self):
        return ",".join([str(r) for r in self.recipients.all()])


