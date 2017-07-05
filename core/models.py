from __future__ import unicode_literals

from django.db import models

from log.models import Business, EmployeeProfile


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
    get_issuers_string.short_description = 'issuers'


class ManagerMessage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(EmployeeProfile, related_name='manager_msg')
    sent_time = models.DateTimeField()
    subject = models.TextField(max_length=50)
    text = models.TextField(max_length=200)

    def get_split_msg(self):
        return self.text.split(':')

    def get_recipients_string(self):
        num_of_recipients = len(self.recipients.all())
        if num_of_recipients > 5:
            return ', '.join(str(emp) for emp in self.recipients.all()[:5]) +\
                   ' and ' + str(num_of_recipients - 5) + ' more'
        return ', '.join(str(emp) for emp in self.recipients.all())
    get_recipients_string.short_description = 'recipients'
