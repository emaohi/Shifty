import datetime

from django.contrib.auth.models import Group, User

from core.date_utils import get_today_day_num_str, get_curr_week_num
from core.models import Shift


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


def set_employee(new_user):
    group, _ = Group.objects.get_or_create(name='Employees')
    group.user_set.add(new_user)
    new_user.profile.role = 'WA'
    new_user.profile.save()


def create_new_manager(cred_dict):
    new_user = User.objects.create_user(**cred_dict)
    set_manager(new_user)
    disable_mailing(new_user)


def create_new_employee(cred_dict):
    new_user = User.objects.create_user(**cred_dict)
    set_employee(new_user)
    disable_mailing(new_user)


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


def set_address_to_employee(username, address):
    user = User.objects.get(username=username)
    profile = user.profile
    profile.home_address = address
    profile.save()


def make_slot_this_in_n_hour_from_now(slot, num_hours):
    slot.day = get_today_day_num_str(datetime.datetime.today().weekday())
    slot.start_hour = (datetime.datetime.now() + datetime.timedelta(hours=num_hours))
    slot.week = get_curr_week_num()
    slot.save()


def create_shifts_for_slots(slots, emps):
    for slot in slots:
        shift = Shift.objects.create(slot=slot)
        shift.employees.add(*list(emps))
        shift.save()
        print '------ shift: %s created' % str(shift)
