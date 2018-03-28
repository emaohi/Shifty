import datetime
import json

import logging
import urllib

import requests
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.utils import timezone

from core.date_utils import get_date, get_curr_week_num, get_next_week_num, get_current_week_range
from core.models import ManagerMessage, EmployeeRequest, Holiday, ShiftSlot, ShiftRequest, Shift
from Shifty.utils import send_multiple_mails_with_html, get_curr_profile
from django.conf import settings

logger = logging.getLogger(__name__)


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


def get_manger_msgs_of_employee(employee, is_new):
    if is_new:
        messages = ManagerMessage.objects.filter(
            recipients__in=[employee]).order_by('-sent_time')[:employee.new_messages]
        return messages

    key = employee.get_manager_msg_cache_key()
    if key not in cache:
        messages = ManagerMessage.objects.filter(
            recipients__in=[employee]).order_by('-sent_time')[employee.new_messages:]
        cache.set(key, list(messages), settings.DURATION_CACHE_TTL)
        logger.debug('Taking old manager messages from DB')
        return messages
    logger.debug('Taking old manager messages from cache')
    return cache.get(key)


def get_employee_requests_with_status(manager, status):
    business_employees = manager.business.get_employees()
    return EmployeeRequest.objects.filter(issuers__in=business_employees, status=status). \
        distinct().order_by('-sent_time')


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

        _, created = Holiday.objects.get_or_create(name=h_name, date=date)
        logger.info('got %s holiday,%r created', h_name, created)


def validate_language(text):
    url = settings.PROFANITY_SERVICE_URL % urllib.quote(text)
    res = requests.get(url)
    if res.text == 'true':
        return False
    return True


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


def get_dist_data(home_address, work_address, arriving_method):
    json_res = {}
    if arriving_method == 'D' or arriving_method == 'B':
        driving_api_url = settings.DISTANCE_URL % (home_address, work_address, 'driving', settings.DISTANCE_API_KEY)
        json_res['driving'] = requests.get(driving_api_url)
        json_res['driving_url'] = settings.DIRECTIONS_URL %\
            (home_address, work_address, 'driving')
    if arriving_method == 'W' or arriving_method == 'B':
        walking_api_url = settings.DISTANCE_URL % (home_address, work_address, 'walking', settings.DISTANCE_API_KEY)
        json_res['walking'] = requests.get(walking_api_url)
        json_res['walking_url'] = settings.DIRECTIONS_URL %\
            (home_address, work_address, 'walking')

    return json_res


def get_week_slots(business, week_num):
    next_week_slots = ShiftSlot.objects.filter(week=week_num, business=business)
    return next_week_slots


def get_current_week_slots(business):
    curr_week_no = get_curr_week_num()
    curr_week_slots = ShiftSlot.objects.filter(week=curr_week_no, business=business)
    return curr_week_slots


def parse_duration_data(raw_distance_response):
    driving_duration = None
    walking_duration = None

    if 'driving' in raw_distance_response:
        try:
            driving_duration = json.loads(raw_distance_response.get('driving').text).get('rows')[0].get(
                'elements')[0].get('duration').get('text')
        except (KeyError, AttributeError) as e:
            logger.warning('couldn\'t get driving duration: ' + str(e))
            driving_duration = ''
    if 'walking' in raw_distance_response:
        try:
            walking_duration = json.loads(raw_distance_response.get('walking').text).get('rows')[0].get(
                'elements')[0].get('duration').get('text')
        except (KeyError, AttributeError) as e:
            logger.warning('couldn\'t get walking duration: ' + str(e))
            walking_duration = ''

    return driving_duration, walking_duration


def save_shifts_request(form, request):
    slots_request = form.save(commit=False)
    slots_request.employee = request.user.profile
    slots_request.submission_time = timezone.localtime(timezone.now())
    slots_request.save()
    form.save_m2m()
    add_mandatory_slots(slots_request)
    return slots_request


def add_mandatory_slots(slot_request):
    business = slot_request.employee.business
    mandatory_slots = ShiftSlot.objects.filter(is_mandatory=True, business=business, week=get_next_week_num())
    slot_request.requested_slots.add(*list(mandatory_slots))


def delete_other_requests(request, slots_request):
    start_week, end_week = get_current_week_range()
    existing_requests = ShiftRequest.objects \
        .filter(employee=get_curr_profile(request),
                submission_time__range=[start_week, end_week]). \
        exclude(submission_time=slots_request.submission_time)
    logger.info("deleting %d old slots for this week...", existing_requests.count())
    existing_requests.delete()


def get_cached_non_mandatory_slots(business, week):

    half_an_hour = 30 * 60
    key = "next-week-slots-{0}-{1}".format(business, week)
    if key not in cache:
        slots = ShiftSlot.objects.filter(week=week, business=business). \
            exclude(is_mandatory=True)
        cache.set(key, slots, half_an_hour)
        return slots
    return cache.get(key)


def get_slot_calendar_colors(curr_profile, slot):
    if curr_profile.role != 'MA':
        bg_color, text_color = ('mediumseagreen', 'white') if curr_profile in \
                                                              slot.shift.employees.all() else ('#7b8a8b', 'black')
    else:
        if slot.is_finished():
            bg_color, text_color = 'cornflowerblue', 'white'
        else:
            bg_color, text_color = 'blue', 'white'
    return bg_color, text_color


def get_eta_cache_key(profile_id):
    return "{0}ETA-{1}".format('TEST-' if settings.TESTING else '', get_curr_profile(profile_id))


def get_next_shift(profile):
    Shift.objects.all().order_by('slot__day', 'slot__ho')
    ordered_current_week_emp_shifts = profile.shifts.filter(slot__week__exact=get_curr_week_num())\
        .order_by('slot__day', 'slot__start_hour')
    for shift in ordered_current_week_emp_shifts:
        if shift.slot.get_datetime() > datetime.datetime.now():
            return shift
    return None


def get_emp_previous_shifts(profile):
    return profile.shifts.filter(slot__week__lt=get_curr_week_num())\
        .order_by('-slot__day', '-slot__start_hour')


def get_logo_url(business_name):
    lookup_url = settings.LOGO_LOOKUP_URL % business_name
    try:
        response = requests.get(lookup_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.findAll("div", {"class": "Logo"})[0].find("img")['src']
    except (KeyError, IndexError):
        raise NoLogoFoundError('Couldn\'t extract image src url from soup...')


def get_next_shifts_of_emp(employee):
    curr_emp_week_slots = ShiftSlot.objects.filter(
        shift__employees__id__iexact=employee.id, week=get_curr_week_num())
    curr_emp_future_slots = [slot for slot in curr_emp_week_slots if not slot.is_finished()]
    return curr_emp_future_slots


def manager_act_on_swap(swap_request, approved):
    recipients = [swap_request.requester, swap_request.responder]
    logger.info('manager %s shift request of %s for %s, sending mails', 'accepted' if approved else 'rejected',
                recipients[0], recipients[1])
    create_manager_msg(recipients=recipients, subject='Manager action', text='Manager acted on swap request',
                       wait_for_mail_results=False)
    if approved:
        swap_shifts(swap_request, *recipients)


def swap_shifts(swap_request, requester, responder):
    logger.info('Going to swap shifts of requester %s and responder %s', requester, responder)
    try:
        with transaction.atomic():
            swap_request.requester_shift.remove_employee(requester)
            swap_request.requester_shift.add_employee(responder)
            swap_request.requested_shift.remove_employee(responder)
            swap_request.requested_shift.add_employee(requester)
        logger.info('Swap completed')
    except IntegrityError as e:
        logger.error('Couldn\'t swap shifts: %s, rolling back accept step', str(e))
        swap_request.accept_step = 1
        swap_request.save()


class NoLogoFoundError(Exception):
    pass



