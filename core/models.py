from __future__ import unicode_literals

from django.db import models

from log.models import Business, EmployeeProfile


class ShiftsArrangement(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    # Json in the structure of:
    # {sunday:[{start:<>, end:<>}, {}, {}...]}, monday: [], ..., saturday:[]}
    arrangement = models.TextField(max_length=200)
    submit_deadline = models.DateTimeField()


class EmployeeRequest(models.Model):

    issuers = models.ManyToManyField(EmployeeProfile, related_name='request_issued')
    sent_time = models.DateTimeField()
    subject = models.TextField(max_length=50)
    text = models.TextField(max_length=200)
    STATUS_CHOICES = (
        ('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def get_issuers_string(self):
        return ', '.join(str(emp) for emp in self.issuers.all())


class ManagerMessage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(EmployeeProfile, related_name='manager_msg')
    sent_time = models.DateTimeField()
    subject = models.TextField(max_length=50)
    text = models.TextField(max_length=200)

    def get_split_msg(self):
        return self.text.split(':')


class ShiftSwapMessage(models.Model):
    sender = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='shift_swap_send')
    receiver = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='shift_swap_receiver')
    sent_time = models.DateTimeField()
