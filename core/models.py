from __future__ import unicode_literals

import datetime
from django.db import models

from core.date_utils import get_next_week_num
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
    TYPE_CHOICES = (
        ('P', 'Profile change'), ('S', 'Shift swap')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='P')

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


class Holiday(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField(primary_key=True)

    def get_holiday_week_no(self):
        base_week_no = self.date.isocalendar()[1]

        is_sunday = True if datetime.datetime.today().weekday() == 6 else False
        return base_week_no if not is_sunday else base_week_no + 1

    def __str__(self):
        return self.name


class ShiftSlot(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    YEAR_CHOICES = [(r, r) for r in range(datetime.date.today().year, datetime.date.today().year + 30)]
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    WEEK_CHOICES = [(w, w) for w in range(1, 53)]
    week = models.IntegerField(choices=WEEK_CHOICES, default=1)

    DAYS_OF_WEEK = (
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday'),
    )
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)

    start_hour = models.TimeField()
    end_hour = models.TimeField()

    constraints = models.TextField(max_length=300)

    holiday = models.ForeignKey(Holiday, blank=True, null=True)

    is_mandatory = models.BooleanField(default=False)

    name = models.CharField(blank=True, null=True, default='Custom', max_length=30)

    def __str__(self):
        return '%s slot - %s, %s to %s%s' %\
               (self.name, self.get_day_str(), str(self.start_hour),
                str(self.end_hour), ' --MANDATORY--' if self.is_mandatory else '')

    def start_time_str(self):
        return '%s %s' % (self.get_date(), self.start_hour)

    def end_time_str(self):
        return '%s %s' % (self.get_date(), self.end_hour)

    def get_date(self):
        correct_week = self.week if int(self.day) > 1 else self.week - 1
        d = '%s-W%s' % (str(self.year), str(correct_week))
        return datetime.datetime.strptime(d + '-%s' % str(int(self.day) - 1), "%Y-W%W-%w").date().strftime('%d-%m-%Y')

    def get_day_str(self):
        return self.get_day_display()

    def is_next_week(self):
        return self.week == get_next_week_num()


# class Shift(models.Model):
#     pass
#
#
class ShiftRequest(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    requested_slots = models.ManyToManyField(ShiftSlot)
    submission_time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return 'request in: ' + str(self.submission_time)

    def get_slots(self):
        return ", ".join([str(slot) for slot in self.requested_slots.all()])
