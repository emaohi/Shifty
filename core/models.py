from __future__ import unicode_literals

import datetime
import json

import logging
from django.db import models

from core.date_utils import get_next_week_num, get_week_range, get_week_string, get_today_date
from log.models import Business, EmployeeProfile

logger = logging.getLogger(__name__)


class EmployeeRequest(models.Model):

    issuers = models.ManyToManyField(EmployeeProfile, related_name='request_issued')
    sent_time = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(max_length=50)
    text = models.TextField(max_length=200)
    STATUS_CHOICES = (
        ('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    TYPE_CHOICES = (
        ('P', 'Profile change'), ('S', 'Shift swap'), ('M', 'Menu test retry'), ('O', 'Other')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='O')

    def get_issuers_string(self):
        return ', '.join(str(emp) for emp in self.issuers.all())
    get_issuers_string.short_description = 'issuers'

    def save(self, *args, **kwargs):
        if not self.subject:
            self.subject = self.get_type_display() + ' subject'
        if not self.text:
            self.text = self.get_type_display() + ' text'
        super(EmployeeRequest, self).save(*args, **kwargs)


class ManagerMessage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(EmployeeProfile, related_name='manager_msg')
    sent_time = models.DateTimeField()
    subject = models.TextField(max_length=50)
    text = models.TextField(max_length=200)

    def get_split_msg(self):
        return self.text.split(':')

    def get_recipients_string(self):
        num_of_recipients = self.recipients.all().count()
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
        return '%s slot(#%s) - %s, %s to %s%s' %\
               (self.name, self.id, self.get_day_str(), str(self.start_hour),
                str(self.end_hour), '(Mandatory)' if self.is_mandatory else '')

    def start_time_str(self):
        return '%s %s' % (self.get_date(), self.start_hour)

    def end_time_str(self):
        return '%s %s' % (self.get_date(), self.end_hour)

    def get_date(self):
        return self.get_date_obj().strftime('%d-%m-%Y')

    def get_datetime(self):
        return datetime.datetime.combine(self.get_date_obj(), self.start_hour)

    def get_date_obj(self):
        correct_week = self.week if int(self.day) > 1 else self.week - 1
        d = '%s-W%s' % (str(self.year), str(correct_week))
        return datetime.datetime.strptime(d + '-%s' % str(int(self.day) - 1), "%Y-W%W-%w").date()

    def get_day_str(self):
        return self.get_day_display()

    def is_next_week(self):
        return self.week == get_next_week_num()

    def get_constraints_json(self):
        return json.loads(self.constraints)

    def get_constraint_num_of_role(self, role):
        return self.get_constraints_json()[role]['num']

    def get_week_str(self):
        return get_week_string(self.week, self.year)

    def was_shift_generated(self):
        return hasattr(self, 'shift')

    def is_finished(self):
        return self.get_datetime() < datetime.datetime.now()


class ShiftRequest(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    requested_slots = models.ManyToManyField(ShiftSlot, related_name='slot_requests')
    submission_time = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        return 'request in: ' + str(self.submission_time)

    def get_slots(self):
        return ", ".join([str(slot) for slot in self.requested_slots.all()])

    def week_range(self):
        start_week, end_week = get_week_range(self.submission_time.date())
        return ' -> '.join([str(start_week), str(end_week)])


class Shift(models.Model):
    slot = models.OneToOneField(ShiftSlot, on_delete=models.CASCADE, related_name='shift', primary_key=False)
    employees = models.ManyToManyField(EmployeeProfile, related_name='shifts')
    rank = models.IntegerField(choices=[(i + 1, i + 1) for i in range(100)], default=50)
    total_tips = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return 'shift of slot: ' + str(self.slot)

    def get_employees_string(self):
        return ", ".join([str(emp) for emp in self.employees.all()])

    def get_date(self):
        return self.slot.get_date()

    def update_emp_rates(self, old_rank):
        new_rank = self.rank / self.employees.count()
        old_rate = old_rank / self.employees.count()
        emps = self.employees.all()
        logger.info('Going to set rate of %f to employees %s', new_rank, emps)
        for emp in emps:
            emp.rate += new_rank - old_rate
            logger.debug('%s employee new rate: %f', emp, emp.rate)
            emp.save()
