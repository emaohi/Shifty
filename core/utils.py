import datetime
import json

import logging

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from core.date_utils import get_date, get_curr_week_num
from core.models import ManagerMessage, EmployeeRequest, Holiday, ShiftSlot
from Shifty.utils import send_multiple_mails_with_html
from django.conf import settings

logger = logging.getLogger('cool')


def create_manager_msg(recipients, subject, text, wait_for_mail_results=True):
    curr_business = recipients.first().business
    manager_msg = ManagerMessage(business=curr_business, sent_time=timezone.now(),
                                 subject=subject, text=text)
    manager_msg.save()

    recipients = recipients.exclude(user=curr_business.manager)
    manager_msg.recipients = recipients
    manager_msg.save()

    # send emails
    recipient_users = [r.user for r in recipients]
    recipient_to_context_dict = {user: {'manager': curr_business.manager.username, 'username': user.first_name}
                                 for user in recipient_users}
    template = 'html_msgs/new_manager_message_email_msg.html'
    mail_subject = 'New message in Shifty app'
    mail_text = 'you\'ve got new message from your manger'

    send_multiple_mails_with_html(subject=mail_subject, text=mail_text,
                                  template=template, r_2_c_dict=recipient_to_context_dict,
                                  wait_for_results=wait_for_mail_results)


def get_manger_msgs_of_employee(employee):
    return ManagerMessage.objects.filter(recipients__in=[employee]).order_by('-sent_time')


def get_employee_requests_with_status(manager, status):
    business_employees = manager.business.get_employees()
    return EmployeeRequest.objects.filter(issuers__in=business_employees, status=status). \
        distinct()


def send_mail_to_manager(emp_user):
    send_multiple_mails_with_html(subject='New message in Shifty app',
                                  text='you\'ve got new message from %s' % emp_user.username,
                                  template='html_msgs/new_employee_change_request.html',
                                  r_2_c_dict={emp_user.profile.get_manager_user():
                                              {'employee_first_name': emp_user.first_name,
                                               'employee_last_name': emp_user.last_name}})


def get_op_and_apply(data, constraint_name):
    role = constraint_name.split('__')[0].split('_')[0]
    field_name = constraint_name.split('__')[0].split('_')[1]
    op = apply_on = ''

    for field in data:
        split_field = field.split('__')
        if split_field[0].split('_')[0] == role and split_field[0].split('_')[1] == field_name:
            action = split_field[1].split('_')[0]
            if action == 'operation':
                op = field
            elif action == 'applyOn':
                apply_on = field
    if op and apply_on:
        return op, apply_on
    else:
        raise Exception('not enough fields for %s' % constraint_name)


def create_constraint_json_from_form(data):
    roles = ['waiter', 'bartender', 'cook']
    constraint_json = {role: {'num': data['num_of_%ss' % role]} for role in roles}

    filtered_constraint_names = [f for f in data if '__' in f]
    for role in roles:
        for constraint_name in filtered_constraint_names:
            if all(x in constraint_name for x in ['val', role]) and data[constraint_name]:
                op, apply_on = get_op_and_apply(data, constraint_name)
                val_content = data[constraint_name]
                constraint_field = constraint_name.split('__')[0].split('_')[1]
                role_json = constraint_json[role]
                role_json[constraint_field] = {'val': val_content, 'op': data[op], 'apply_on': data[apply_on]}
    return constraint_json


def save_holidays(holiday_json):
    holiday_list = json.loads(holiday_json)['items']
    for holiday in holiday_list:
        h_name = holiday.get('title')
        h_date = holiday.get('date')
        date = datetime.datetime.strptime(h_date, '%Y-%m-%d')

        new_holiday = Holiday(name=h_name, date=date)
        new_holiday.save()


def get_holiday_or_none(year, day, week):
    if day == '':
        return None
    try:
        slot_holiday = Holiday.objects.get(date=get_date(year, day, week))
    except ObjectDoesNotExist:
        slot_holiday = None
    return slot_holiday


def get_color_and_title_from_slot(slot):
    name = slot.name
    is_holiday = 'holiday' if slot.holiday else ''
    title = '%s%s (%s)' % (name, is_holiday, slot.id)
    text_color = '#f5dd5d' if not (slot.is_mandatory or slot.holiday) else '#ff0000'

    return text_color, title


def duplicate_favorite_slot(business, name):
    template_slot = ShiftSlot.objects.filter(business=business, name=name).first()
    template_slot.id = None
    template_slot.save()
    return template_slot


def handle_named_slot(business, name):
    pinned_slot = duplicate_favorite_slot(business, name)
    pinned_slot.week = get_curr_week_num() - 5
    pinned_slot.save()


def get_dist_data(home_address, work_address, is_drive, is_walk):
    json_res = {}
    if is_drive:
        driving_api_url = settings.DISTANCE_URL % (home_address, work_address, 'driving', settings.DISTANCE_API_KEY)
        json_res['driving'] = requests.get(driving_api_url)
    if is_walk:
        walking_api_url = settings.DISTANCE_URL % (home_address, work_address, 'walking', settings.DISTANCE_API_KEY)
        json_res['walking'] = requests.get(walking_api_url)

    return json_res


def get_parsed_duration_data(raw_distance_response):
    parsed_durations = {}
    driving_duration = None
    walking_duration = None
    if 'driving' in raw_distance_response:
        try:
            driving_duration = json.loads(raw_distance_response.get('driving').text).get('rows')[0].get(
                'elements')[0].get('duration').get('text')
        except KeyError as e:
            logger.warning('couldn\'t get driving duration: ' + str(e))
            driving_duration = ''
        finally:
            parsed_durations['driving'] = driving_duration
    if 'walking' in raw_distance_response:
        try:
            walking_duration = json.loads(raw_distance_response.get('walking').text).get('rows')[0].get(
                'elements')[0].get('duration').get('text')
        except KeyError as e:
            logger.warning('couldn\'t get walking duration: ' + str(e))
            walking_duration = ''
        finally:
            parsed_durations['walking'] = walking_duration

    return parsed_durations


