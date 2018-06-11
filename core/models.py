from __future__ import unicode_literals
from __future__ import division

import datetime
import json

import logging

from django.db import models, IntegrityError, transaction
from django.db.models import F
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from Shifty.utils import get_time_from_str
from core.date_utils import get_next_week_num, get_week_range, get_week_string
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

    class Meta:
        ordering = ['-sent_time']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['status']),
        ]

    def get_issuers_string(self):
        return ', '.join(str(emp) for emp in self.issuers.all())
    get_issuers_string.short_description = 'issuers'

    def is_shift_swap(self):
        return self.type == 'S'

    def is_accepted(self):
        return self.status == 'A'

    def is_rejected(self):
        return self.status == 'R'

    def business(self):
        return self.issuers.first().business

    def save(self, *args, **kwargs):
        if not self.subject:
            self.subject = self.get_type_display() + ' subject'
        if not self.text:
            self.text = self.get_type_display() + ' text'

        if self.is_shift_swap() and hasattr(self, 'swap_request'):
            if self.is_accepted():
                logger.info('Accepting shift swap request !')
                self.swap_request.accept_step = 2
            elif self.is_rejected():
                logger.info('Rejecting shift swap request !')
                self.swap_request.accept_step = -2
            self.swap_request.save()

        super(EmployeeRequest, self).save(*args, **kwargs)


class ManagerMessage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(EmployeeProfile, related_name='manager_msg')
    sent_time = models.DateTimeField(auto_now_add=True)
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


class SavedSlot(models.Model):
    name = models.CharField(max_length=30, unique=True)
    constraints = models.TextField(max_length=300)
    is_mandatory = models.BooleanField(default=False)

    def __str__(self):
        return 'saved shift slot %s, constraints: %s' % (self.name, self.constraints)


class ShiftSlot(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    YEAR_CHOICES = [(r, r) for r in range(datetime.date.today().year, datetime.date.today().year + 30)]
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    WEEK_CHOICES = [(w, w) for w in range(1, 53)]
    week = models.IntegerField(choices=WEEK_CHOICES, default=1, db_index=True)

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

    name = models.CharField(blank=True, null=True, max_length=30)

    saved_slot = models.ForeignKey(SavedSlot, null=True, blank=True)

    def __str__(self):
        return '%s slot(#%s) - %s, %s to %s%s' %\
               (self.name, self.id, self.get_day_str(), self.get_datetime_str(),
                str(self.end_hour), '(Mandatory)' if self.is_mandatory else '')

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.saved_slot:
                self._update_saved_slot_upon_creation()
            else:
                self.name = self.name if self.name else 'Custom'
        else:
            if self.saved_slot:
                self._validate_saved_slot_fields_maintained()
            else:
                self.name = self.name if self.name else 'Custom'

        super(ShiftSlot, self).save(*args, **kwargs)

    def _update_saved_slot_upon_creation(self):
        fields = ['name', 'constraints', 'is_mandatory']
        for field in fields:
            setattr(self, field, getattr(self.saved_slot, field))
        logger.debug('updated %s fields of slot %s', fields, self)

    def _validate_saved_slot_fields_maintained(self):
        fields = ['name', 'constraints', 'is_mandatory']
        logger.debug('validating %s fields of slot %s not changed', fields, self)
        for field in fields:
            if getattr(self, field) != getattr(self.saved_slot, field):
                raise IntegrityError('field %s of slot %s is different from same field in saved-slot %s' %
                                     (field, self, self.saved_slot))

    def start_time_str(self):
        return '%s %s' % (self.get_date(), self.start_hour)

    def end_time_str(self):
        return '%s %s' % (self.get_date(), self.end_hour)

    def get_date(self):
        return self.get_date_obj().strftime('%d-%m-%Y')

    def get_datetime_str(self):
        return self.get_datetime().strftime('%d-%m-%Y, %H:%M')

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

    def get_color_and_title(self):
        holiday_str = ' holiday' if self.holiday else ''
        title = '%s%s (%s)' % (self.name, holiday_str, self.id)
        text_color = '#f5dd5d' if not (self.is_mandatory or self.holiday) else '#ff0000'
        return text_color, title

    def get_calendar_colors(self, curr_profile):
        if curr_profile.role != 'MA':
            bg_color, text_color = ('mediumseagreen', 'white') if curr_profile in \
                                                                  self.shift.employees.all() else ('#7b8a8b', 'black')
        else:
            if self.is_finished():
                bg_color, text_color = 'cornflowerblue', 'white'
            else:
                bg_color, text_color = 'blue', 'white'
        return bg_color, text_color

    def get_time_frame_code(self):
        current_day_multiply = int(self.day) * 2
        return current_day_multiply if self.start_hour > get_time_from_str('15:00') else\
            current_day_multiply - 1

    def delete_existing_shift(self):
        if hasattr(self, 'shift'):
            logger.debug('Going to delete shift for slot %s', self)
            self.shift.delete()
        else:
            logger.debug('no old shift for slot %s', self)

    def is_emp_requested(self, emp):
        return self.slot_requests.filter(employee=emp).exists()


class ShiftRequest(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    requested_slots = models.ManyToManyField(ShiftSlot, related_name='slot_requests', blank=True)
    submission_time = models.DateTimeField(auto_now=True, )
    is_automatic = models.BooleanField(default=False)

    def __str__(self):
        return 'request in: ' + str(self.submission_time)

    def get_slots(self):
        return ", ".join([str(slot) for slot in self.requested_slots.all()])

    def week_range(self):
        start_week, end_week = get_week_range(self.submission_time.date())
        return ' -> '.join([str(start_week), str(end_week)])

    def add_mandatory_slots(self):
        mandatory_slots = ShiftSlot.objects.filter(is_mandatory=True, business=self.employee.business,
                                                   week=get_next_week_num())
        logger.debug('mandatory slots are %s', mandatory_slots)
        mandatory_slots = list(mandatory_slots)
        self.requested_slots.add(*mandatory_slots)

    def add_preferred_slots(self):
        next_week_non_mandatory_slots = ShiftSlot.objects.filter(week=get_next_week_num(),
                                                                 business=self.employee.business)\
            .exclude(is_mandatory=True)
        relevant_slots = [slot for slot in next_week_non_mandatory_slots if
                          slot.get_time_frame_code() in self.employee.get_preferred_time_frame_codes()]
        logger.info('Going to add slots to automatic slots request of emp %s: %s', self.employee, relevant_slots)
        for slot in relevant_slots:
            self.requested_slots.add(slot)


class Shift(models.Model):
    slot = models.OneToOneField(ShiftSlot, on_delete=models.CASCADE, related_name='shift', primary_key=False)
    employees = models.ManyToManyField(EmployeeProfile, related_name='shifts')
    rank = models.IntegerField(choices=[(i + 1, i + 1) for i in range(100)], default=50)
    total_tips = models.IntegerField(default=0)
    remarks = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return 'shift of slot: ' + str(self.slot)

    def add_employee(self, emp):
        self.employees.add(emp)

    def remove_employee(self, emp):
        if not self.emp_exists(emp):
            logger.warning('Trying to remove not existing employee %s from shift %s', emp, self)
        self.employees.remove(emp)

    def get_employees_string(self):
        return ", ".join([str(emp) for emp in self.employees.all()])

    def get_date(self):
        return self.slot.get_date()

    def calculate_employee_tip(self):
        try:
            return self.total_tips / self.employees.count()
        except ZeroDivisionError:
            logger.warning('Trying to calculate tips for shift without employees')
            return 'No employees for this shift'

    def get_employees_comma_string(self):
        return ', '.join([emp.user.username for emp in self.employees.all()])

    def emp_exists(self, emp):
        return emp in self.employees.all()


class ShiftSwap(models.Model):
    requester = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='SwapRequesting')
    responder = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='SwapRequested')

    requester_shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='SwapRequesting')
    requested_shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='SwapRequested')

    ACCEPT_STEP_OPTIONS = (
        (0, 'employee requested'),
        (1, 'employee accepted'),
        (2, 'manager accepted'),
        (-1, 'employee rejected'),
        (-2, 'manager rejected'),
    )
    accept_step = models.IntegerField(choices=ACCEPT_STEP_OPTIONS, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    employee_request = models.OneToOneField(EmployeeRequest, on_delete=models.CASCADE,
                                            null=True, blank=True, related_name='swap_request')

    def __str__(self):
        return 'swap request from %s to %s' % (self.requester, self.responder)

    def save(self, *args, **kwargs):
        if self.accept_step == 1:
            logger.debug('saved shiftSwap of status 1, going to create employeeRequest')
            self.employee_request = EmployeeRequest.objects.create(type='S')
            self.employee_request.issuers.add(self.requester, self.responder)
        elif self.accept_step == 2 or self.accept_step == -2:
            logger.debug('saved shiftSwap of status %d', self.accept_step)
            self.handle_manager_action(self.accept_step)
        super(ShiftSwap, self).save(*args, **kwargs)

    def handle_manager_action(self, manager_action):
        approved = manager_action == 2
        manager_action = 'accepted' if approved else 'rejected'
        logger.info('manager %s shift request of %s for %s, sending mails', manager_action,
                    self.requester, self.responder)
        logger.info('Going to flush old swap requests form swap employees')
        self.flush_swap_request_cache_of_employees()
        if approved:
            try:
                self.swap_shifts()
                logger.info('Swap completed')
            except IntegrityError as e:
                logger.error('Couldn\'t swap shifts: %s, rolling back accept step', str(e))
                self.accept_step = 1
                self.save()

    def swap_shifts(self):
        logger.info('Going to swap shifts of requester %s and responder %s', self.requester, self.responder)
        with transaction.atomic():
            self.requester_shift.remove_employee(self.requester)
            self.requester_shift.add_employee(self.responder)
            self.requested_shift.remove_employee(self.responder)
            self.requested_shift.add_employee(self.requester)

    def flush_swap_request_cache_of_employees(self):
        self.responder.flush_swap_requests_cache()
        self.requester.flush_swap_requests_cache()

    def is_open(self):
        return self.accept_step in self.open_accept_steps()

    @staticmethod
    def open_accept_steps():
        return [0, 1]

    @staticmethod
    def closed_accept_steps():
        return [-2, -1, 2]

    class Meta:
        unique_together = (('requester', 'requester_shift'), ('requester', 'requested_shift'))


# pylint: disable=unused-argument
@receiver(m2m_changed, sender=ManagerMessage.recipients.through)
def update_employee(sender, **kwargs):
    logger.info('incrementing new message for employees in message')
    kwargs.pop('instance').recipients.all().update(new_messages=F('new_messages') + 1)


# pylint: disable=unused-argument
@receiver(post_save, sender=Shift)
def update_employee_rates(sender, **kwargs):
    shift = kwargs.pop('instance')
    if shift.employees.exists():
        adding_val = shift.rank/shift.employees.count()
        logger.info('in Shift model post_save signal, incrementing rates of employees by %s...', adding_val)
        for emp in shift.employees.all():
            emp.rate += adding_val
            emp.save()
    else:
        logger.debug('saving shift without employees(yet)...')
