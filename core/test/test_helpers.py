import datetime
import json

import mock
from django.contrib.auth.models import Group, User

from Shifty.utils import get_time_from_str
from core.date_utils import get_today_day_num_str, get_curr_week_num, get_curr_year, get_next_week_num
from core.models import Shift, ShiftSlot


def create_manager_and_employee_groups():
    Group.objects.create(name='Employees')
    Group.objects.create(name='Managers')


def set_manager(new_user):
    group, _ = Group.objects.get_or_create(name='Managers')
    group.user_set.add(new_user)
    new_user.profile.role = 'MA'
    new_user.profile.save()
    new_user.profile.business.manager = new_user
    new_user.profile.business.save()


def set_employee(new_user, role):
    group, _ = Group.objects.get_or_create(name='Employees')
    group.user_set.add(new_user)
    new_user.profile.role = role
    new_user.profile.save()


def create_new_manager(cred_dict):
    new_user = User.objects.create_user(**cred_dict)
    set_manager(new_user)
    disable_mailing(new_user)


def create_new_employee(cred_dict, role='WA'):
    new_user = User.objects.create_user(**cred_dict)
    set_employee(new_user, role)
    disable_mailing(new_user)
    return new_user.profile


def create_multiple_employees(num):
    print 'creating %d employees...' % num
    new_emps = []
    for i in range(num):
        cred_dict = {'username': 'test_user_%d' % i, 'password': 'secret'}
        new_emps.append(create_new_employee(cred_dict))
    return new_emps


def create_slots_for_next_week(business, waiter='1', bartender='1', cook='1', num=1):
    slots = []
    for i in range(num):
        s = ShiftSlot.objects.create(business=business, year=get_curr_year(), week=get_next_week_num(),
                                     day=str(i+1), start_hour=get_time_from_str('16:00'),
                                     end_hour=get_time_from_str('17:00'))
        s.constraints = json.dumps({'waiter': {'num': waiter}, 'bartender': {'num': bartender},
                                    'cook': {'num': cook}})
        s.save()
        slots.append(s)

    return slots


def disable_mailing(user):
    user.profile.enable_mailing = False
    user.profile.save()


def add_fields_to_slot(slot):
    for role in ['waiter', 'bartender', 'cook']:
        for field in ['gender', 'age', 'average_rate', 'months_working']:
            slot[role + '_' + field + '__value_constraint'] = ''
            slot[role + '_' + field + '__applyOn_constraint'] = ''
            slot[role + '_' + field + '__operation_constraint'] = ''


def set_address_to_business(username, address):
    user = User.objects.get(username=username)
    business = user.profile.business
    business.address = address
    business.save()


def get_business_of_username(username):
    user = User.objects.get(username=username)
    return user.profile.business


def set_address_to_employee(username, address):
    user = User.objects.get(username=username)
    profile = user.profile
    profile.home_address = address
    profile.save()


def make_slot_this_in_n_hour_from_now(slot, num_hours):
    slot.day = get_today_day_num_str(datetime.datetime.today().weekday())
    slot.start_hour = (datetime.datetime.now() + datetime.timedelta(hours=num_hours)).time()
    slot.week = get_curr_week_num()
    slot.save()


def create_shifts_for_slots(slots, emps):
    for slot in slots:
        shift = Shift.objects.create(slot=slot)
        shift.employees.add(*list(emps))
        shift.save()
        print '------ shift: %s created' % str(shift)


class CatchSignal:
    def __init__(self, signal):
        self.signal = signal
        self.handler = mock.Mock()

    def __enter__(self):
        self.signal.connect(self.handler)
        return self.handler

    def __exit__(self, exc_type, exc_value, tb):
        self.signal.disconnect(self.handler)
