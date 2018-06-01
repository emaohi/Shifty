from __future__ import unicode_literals, division

import json
import urllib2
from datetime import datetime
from urlparse import urlparse

import logging

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.date_utils import get_curr_week_num

logger = logging.getLogger(__name__)


class Business(models.Model):
    business_name = models.CharField(primary_key=True, max_length=30)

    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    BUSINESS_TYPE_CHOICES = (
        ('RE', 'Restaurant'), ('CA', 'Cafe'), ('PU', 'Pub')
    )
    business_type = models.CharField(
        max_length=2,
        choices=BUSINESS_TYPE_CHOICES,
        default='CA',
    )

    address = models.CharField(max_length=30, blank=True, null=True)

    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    TIP_METHOD_CHOICES = (
        ('P', 'Personal'), ('G', 'Group')
    )

    tip_method = models.CharField(max_length=1, choices=TIP_METHOD_CHOICES, default='G')

    DAYS_OF_WEEK = (
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday'),
    )
    deadline_day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, default='7')
    slot_request_enabled = models.BooleanField(default=False)

    SHIFT_GENERATION_STATUS = (
        ('0', 'Not generated'),
        ('1', 'Generated'),
        ('2', 'Failed'),
        ('3', 'Generating')
    )
    shifts_generated = models.CharField(max_length=1, choices=SHIFT_GENERATION_STATUS, default='0')

    def __str__(self):
        return self.business_name

    def get_type(self):
        return self.get_business_type_display()

    def get_employees(self):
        return self.employeeprofile_set.all().prefetch_related('user')

    def get_role_employees(self, role):
        return self.get_employees().filter(role=EmployeeProfile.get_roles_reversed()[role.title()])

    def get_waiters(self):
        return self.get_role_employees('waiter')

    def get_bartenders(self):
        return self.get_role_employees('bartender')

    def get_cooks(self):
        return self.get_role_employees('cook')

    def has_deadline_day_passed(self):
        today_weekday = datetime.today().weekday() + 2
        today_weekday = 1 if today_weekday == 8 else today_weekday
        today_weekday = 2 if today_weekday == 9 else today_weekday

        return today_weekday >= int(self.deadline_day)

    def set_shift_generation_success(self):
        self.shifts_generated = '1'

    def set_shift_generation_failure(self):
        self.shifts_generated = '2'

    def set_shift_generation_pending(self):
        self.shifts_generated = '3'

    def reset_shift_generation_status(self):
        self.shifts_generated = '0'

    def save_logo_from_url(self, url):
        name = urlparse(url).path.split('/')[-1]
        content = ContentFile(urllib2.urlopen(url).read())
        self.logo.save(name, content, save=False)

    def get_next_week_slots_cache_key(self, week):
        return "next-week-slots-{0}-{1}".format(self, week)

    def get_cached_next_week_slots(self, week):
        from core.models import ShiftSlot
        key = self.get_next_week_slots_cache_key(week)
        if key not in cache:
            slots = ShiftSlot.objects.filter(week=week, business=self, is_mandatory=False)
            cache.set(key, slots, settings.DURATION_CACHE_TTL)
            return slots
        return cache.get(key)


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^05\d{1}-\d{7}$',
                                 message="Wrong phone number format.")
    phone_num = models.CharField(validators=[phone_regex], blank=True, max_length=16)  # validators should be a list
    home_address = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    started_work_date = models.DateField(null=True, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'), ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    ROLE_CHOICES = (
        ('MA', 'Manager'), ('WA', 'Waiter'), ('BT', 'Bartender'), ('CO', 'Cook')
    )

    rate = models.FloatField(default=0)

    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default='WA',
    )
    enable_mailing = models.BooleanField(default=True)
    menu_score = models.IntegerField(null=True, blank=True)

    ever_logged_in = models.BooleanField(default=False)
    ARRIVAL_METHOD_CHOCIES = (
        ('D', 'driving'), ('W', 'walking'), ('B', 'both')
    )
    arriving_method = models.CharField(max_length=1, choices=ARRIVAL_METHOD_CHOCIES, default='D')
    new_messages = models.IntegerField(default=0)
    preferred_shift_time_frames = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    # noinspection PyTypeChecker
    def get_employment_months(self):
        if self.started_work_date:
            today = datetime.now().date()
            delta = today - self.started_work_date
            return round(delta.days / 30, 1)
        return None

    def get_age(self):
        if self.birth_date:
            today = datetime.now().date()
            delta = today - self.birth_date
            return round(delta.days / 365, 2)
        return None

    def get_manager(self):
        profile_business = self.business
        for profile in profile_business.employeeprofile_set.all():
            if profile.role == 'MA':
                return profile
        return None

    def get_manager_user(self):
        if self.get_manager():
            return self.get_manager().user

    def get_manger_msgs_of_employee(self, is_new):
        from core.models import ManagerMessage
        if is_new:
            messages = ManagerMessage.objects.filter(
                recipients__in=[self]).order_by('-sent_time')[:self.new_messages]
            return messages

        key = self.get_old_manager_msgs_cache_key()
        if key not in cache:
            messages = ManagerMessage.objects.filter(
                recipients__in=[self]).order_by('-sent_time')[self.new_messages:]
            cache.set(key, list(messages), settings.DURATION_CACHE_TTL)
            logger.debug('Taking old manager messages from DB: %s', messages)
            return messages
        logger.debug('Taking old manager messages from cache')
        return cache.get(key)

    def send_mail_to_manager(self):
        from Shifty.utils import send_multiple_mails_with_html
        send_multiple_mails_with_html(subject='New message in Shifty app',
                                      text='you\'ve got new message from %s' % self.user.username,
                                      template='html_msgs/new_employee_change_request.html',
                                      r_2_c_dict={self.get_manager_user():
                                                      {'employee_first_name': self.user.first_name,
                                                       'employee_last_name': self.user.last_name}})

    def flush_new_messages(self):
        if self.new_messages > 0:
            logger.debug('flushing cache of old manager msgs of emp %s', self)
            cache.delete(self.get_old_manager_msgs_cache_key())
        self.new_messages = 0
        self.save()

    def flush_swap_requests_cache(self):
        logger.debug('flushing cache of old swap requests of emp %s', self)
        cache.delete(self.get_old_swap_requests_cache_key())

    def get_old_manager_msgs_cache_key(self):
        if self.role == 'MA':
            raise ValueError('Can\'t manager messages key of emp %s - is manager' % self)
        return "{0}-old-manager-messages".format(self)

    def get_old_swap_requests_cache_key(self):
        if self.role == 'MA':
            raise ValueError('Can\'t swap requests key of emp %s - is manager' % self)
        return "{0}-old-swap-requests".format(self)

    def get_old_employee_requests_cache_key(self):
        if self.role != 'MA':
            raise ValueError('Can\'t employee requests key of emp %s - is not manager' % self)
        return "{0}-old-emp-requests".format(self)

    def get_eta_cache_key(self):
        return "{0}DURATION-ETA-{1}".format('TEST-' if settings.TESTING else '', self)

    def get_current_week_slots(self):
        from core.models import ShiftSlot
        curr_emp_week_slots = ShiftSlot.objects.filter(
            shift__employees__id__iexact=self.id, week=get_curr_week_num())
        curr_emp_future_slots = [slot for slot in curr_emp_week_slots if not slot.is_finished()]
        return curr_emp_future_slots

    def get_next_shifts(self):
        from core.models import Shift
        Shift.objects.all().order_by('slot__day', 'slot__ho')
        ordered_current_week_emp_shifts = self.shifts.filter(slot__week__exact=get_curr_week_num()) \
            .order_by('slot__day', 'slot__start_hour')
        return [shift for shift in ordered_current_week_emp_shifts if not shift.slot.is_finished()]

    def get_next_shift(self):
        next_shifts = self.get_next_shifts()
        if len(next_shifts) == 0:
            return None
        return next_shifts[0]

    def get_previous_shifts(self):
        return self.shifts.filter(slot__week__lt=get_curr_week_num()) \
            .order_by('-slot__day', '-slot__start_hour')\
            .select_related('slot').prefetch_related(Prefetch('employees',
                                                              queryset=EmployeeProfile.objects.select_related('user')))

    def get_preferred_time_frame_codes(self):
        return [p['id'] for p in json.loads(self.preferred_shift_time_frames)] \
            if self.preferred_shift_time_frames else []

    @classmethod
    def get_roles_reversed(cls):
        return dict((v, k) for k, v in cls.ROLE_CHOICES)

    @classmethod
    def get_employee_roles(cls):
        return [verbose for short, verbose in cls.ROLE_CHOICES if short != 'MA']

    @staticmethod
    def get_filtered_upon_fields():
        return ['birth_date', 'started_work_date', 'gender', 'rate']


# pylint: disable=unused-argument,unused-variable
@receiver(post_save, sender=User)
def update_employee(sender, instance, created, **kwargs):
    if created:
        b, created2 = Business.objects.update_or_create(business_name='dummy')
        EmployeeProfile.objects.create(user=instance, business=b)
    instance.profile.save()
