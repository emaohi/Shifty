import itertools

import datetime
import json
import time
from django.utils import timezone

from core.models import ManagerMessage, EmployeeRequest, Holiday
from Shifty.utils import send_multiple_mails_with_html


def create_manager_msg(recipients, subject, text):
    curr_business = recipients.first().business
    manager_msg = ManagerMessage(business=curr_business, sent_time=timezone.now(),
                                 subject=subject, text=text)
    manager_msg.save()

    manager_msg.recipients = recipients
    manager_msg.save()

    # # send emails
    recipient_users = [r.user for r in recipients]
    recipient_to_context_dict = dict(zip(recipient_users,
                                         itertools.repeat({'manager': curr_business.manager.username})))
    template = 'html_msgs/new_manager_message_email_msg.html'
    subject = 'New message in Shifty app'
    text = 'you\'ve got new message from your manger'

    send_multiple_mails_with_html(subject=subject, text=text,
                                  template=template, r_2_c_dict=recipient_to_context_dict)


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
                                  r_2_c_dict={emp_user.profile.business.manager:
                                                  {'employee_first_name': emp_user.first_name,
                                                   'employee_last_name': emp_user.last_name}})


def get_days_range_by_week_num(week_no, year_no):
    curr_week = "%s-W%s" % (year_no, str(week_no))
    prev_week = "%s-W%s" % (year_no, str(week_no-1))
    sunday = str(datetime.datetime.strptime(prev_week + '-0', "%Y-W%W-%w").date().strftime("%d/%m/%Y"))
    saturday = str(datetime.datetime.strptime(curr_week + '-6', "%Y-W%W-%w").date().strftime("%d/%m/%Y"))

    return '%s --> %s' % (sunday, saturday)


def get_current_week_string():
    curr_year = datetime.datetime.now().year
    week_no = datetime.date.today().isocalendar()[1]
    return get_days_range_by_week_num(week_no, curr_year)


def get_next_week_string():
    curr_year = datetime.datetime.now().year
    week_no = datetime.date.today().isocalendar()[1] + 1
    return get_days_range_by_week_num(week_no, curr_year)


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
