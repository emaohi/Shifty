import datetime
import json

import logging
import urllib

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.utils import timezone
from django_redis import get_redis_connection

from core.date_utils import get_date, get_next_week_num, get_curr_year
from core.models import ManagerMessage, EmployeeRequest, Holiday, ShiftSlot, SavedSlot
from Shifty.utils import send_multiple_mails_with_html
from django.conf import settings

logger = logging.getLogger(__name__)


def create_manager_msg(recipients, subject, text, wait_for_mail_results=True):
    curr_business = recipients.first().business
    manager_msg = ManagerMessage.objects.create(business=curr_business, sent_time=timezone.now(),
                                                subject=subject, text=text)
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


def get_employee_requests_with_status(manager, *statuses):
    business_employees = manager.business.get_employees()
    return EmployeeRequest.objects.filter(issuers__in=business_employees, status__in=[status for status in statuses]). \
        distinct().order_by('-sent_time').prefetch_related('issuers__user')


class SlotConstraintCreator:

    def __init__(self, data):
        self.slot_form_data = data

    def create(self):
        roles = ['waiter', 'bartender', 'cook']
        constraint_json = {role: {'num': self.slot_form_data['num_of_%ss' % role]} for role in roles}

        filtered_constraint_names = [f for f in self.slot_form_data if '__' in f]
        for role in roles:
            for constraint_name in filtered_constraint_names:
                if all(x in constraint_name for x in ['val', role]) and self.slot_form_data[constraint_name]:
                    op, apply_on = self._get_op_and_apply(constraint_name)
                    val_content = self.slot_form_data[constraint_name]
                    constraint_field = constraint_name.split('__')[0].split('_')[1]
                    role_json = constraint_json[role]
                    role_json[constraint_field] = {'val': val_content, 'op': self.slot_form_data[op], 'apply_on': self.slot_form_data[apply_on]}
        return constraint_json

    def _get_op_and_apply(self, constraint_name):
        role = constraint_name.split('__')[0].split('_')[0]
        field_name = constraint_name.split('__')[0].split('_')[1]
        op = apply_on = ''

        for field in self.slot_form_data:
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


def save_holidays(holiday_json):
    holiday_list = json.loads(holiday_json)['items']
    for holiday in holiday_list:
        h_name = holiday.get('title')
        h_date = holiday.get('date')
        date = datetime.datetime.strptime(h_date, '%Y-%m-%d')

        _, created = Holiday.objects.get_or_create(name=h_name, date=date)
        logger.info('got %s holiday,%r created', h_name, created)


class LanguageValidator:
    def __init__(self, url):
        self.checker_url = url

    def validate(self, text):
        url = self.checker_url % urllib.quote(text)
        res = requests.get(url)
        if res.text == 'true':
            return False
        return True


class SlotCreator:
    def __init__(self, business, slot_data, constraint_creator):
        self.business = business
        self.slot_data = slot_data
        self.constraint_creator = constraint_creator
        self.native_redis_client = RedisNativeHandler()

    def create(self):
        if self.slot_data['name'] == '':
            self._create_new_slot()
        else:
            self._create_saved_slot()

    def _create_new_slot(self):
        slot_constraint_json = self.constraint_creator.create()
        slot_holiday = get_holiday(get_curr_year(), self.slot_data['day'], get_next_week_num())
        new_slot = ShiftSlot(business=self.business, day=self.slot_data['day'],
                             start_hour=self.slot_data['start_hour'], end_hour=self.slot_data['end_hour'],
                             week=get_next_week_num(), holiday=slot_holiday)

        if self.slot_data.get('save_as') != '':
            self._create_slot_with_name(new_slot, slot_constraint_json)
        else:
            self._create_new_slot_without_name(new_slot, slot_constraint_json)

    def _create_saved_slot(self):
        saved_slot = SavedSlot.objects.get(name=self.slot_data['name'])
        logger.info('Going to create slot from existing saved slot: %s', saved_slot)
        ShiftSlot.objects.create(business=self.business, day=self.slot_data['day'], week=get_next_week_num(),
                                 start_hour=self.slot_data['start_hour'],
                                 end_hour=self.slot_data['end_hour'], saved_slot=saved_slot)

    def _create_slot_with_name(self, new_slot, slot_constraint_json):
        slot_name = self.slot_data.get('save_as')
        logger.info('Going to create/update named slot with name %s', slot_name)
        new_saved_slot, created = SavedSlot.objects.update_or_create(name=slot_name,
                                                                     defaults={
                                                                        'constraints': json.dumps(slot_constraint_json),
                                                                        'is_mandatory': self.slot_data['mandatory']
                                                                         })
        logger.debug('saved slot %s', 'created' if created else 'updated')
        if created:
            logger.debug('adding slot name %s to cache set', slot_name)
            self.native_redis_client.add_to_set(self.business.get_slot_names_cache_key(), slot_name)
        new_slot.saved_slot = new_saved_slot
        new_slot.save()

    def _create_new_slot_without_name(self, new_slot, slot_constraint_json):
        logger.info('Going to create custom slot: %s', self.slot_data['save_as'])
        new_slot.constraints = json.dumps(slot_constraint_json)
        new_slot.is_mandatory = self.slot_data['mandatory']
        new_slot.save()


def get_holiday(year, day, week):
    if day == '':
        return None
    try:
        slot_holiday = Holiday.objects.get(date=get_date(year, day, week))
    except ObjectDoesNotExist:
        slot_holiday = None
    return slot_holiday


class DurationApiClient:

    def __init__(self, home_address, business_address):
        self.home_address = home_address
        self.business_address = business_address

    def get_dist_data(self, arriving_method):
        json_res = {}
        if arriving_method == 'D' or arriving_method == 'B':
            driving_api_url = settings.DISTANCE_URL % (self.home_address, self.business_address, 'driving',
                                                       settings.DISTANCE_API_KEY)
            json_res['driving'] = requests.get(driving_api_url)
        if arriving_method == 'W' or arriving_method == 'B':
            walking_api_url = settings.DISTANCE_URL % (self.home_address, self.business_address, 'walking',
                                                       settings.DISTANCE_API_KEY)
            json_res['walking'] = requests.get(walking_api_url)
            json_res['walking_url'] = settings.DIRECTIONS_URL %\
                (self.home_address, self.business_address, 'walking')

        driving_str, walking_str = self._parse_duration_data(json_res)

        return dict(driving_url=settings.DIRECTIONS_URL % (self.home_address, self.business_address, 'driving'),
                    walking_url=settings.DIRECTIONS_URL % (self.home_address, self.business_address, 'walking'),
                    driving=driving_str, walking=walking_str)

    def _parse_duration_data(self, raw_distance_response):
        logger.debug('parsing raw response: %s', raw_distance_response)
        driving_duration = None
        walking_duration = None
        if 'driving' in raw_distance_response:
            driving_duration = self._parse_specific_method_duration(raw_distance_response, 'driving')
        if 'walking' in raw_distance_response:
            walking_duration = self._parse_specific_method_duration(raw_distance_response, 'walking')
        return driving_duration, walking_duration

    @staticmethod
    def _parse_specific_method_duration(raw_distance_response, method):
        try:
            duration = json.loads(raw_distance_response.get(method).text).get('rows')[0].get(
                'elements')[0].get('duration').get('text')
        except (KeyError, AttributeError) as e:
            logger.warning('couldn\'t get %s duration: %s', method,  e)
            duration = ''
        return duration


def save_shifts_request(form, profile):
    slots_request = form.save(commit=False)
    slots_request.employee = profile
    slots_request.save()
    form.save_m2m()
    slots_request.add_mandatory_slots()
    slots_request.add_preferred_slots()
    return slots_request


class LogoUrlFinder:
    def __init__(self, url):
        self.logos_site_url = url

    def find_logo(self, business_name):
        lookup_url = self.logos_site_url % business_name
        logger.debug('Going to fetch page at url %s', lookup_url)
        try:
            response = requests.get(lookup_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.findAll("div", {"class": "Logo"})[0].find("img")['src']
        except (KeyError, IndexError) as e:
            raise NoLogoFoundError('Couldn\'t extract image src url from soup... %s' % str(e))


def get_business_slot_names(business):
    key = business.get_slot_names_cache_key()
    redis_handler = RedisNativeHandler()
    if key not in cache:
        slot_names = {t['name'] for t in ShiftSlot.objects.filter(business=business)
                      .values('name').distinct() if t['name'] != 'Custom'}
        if slot_names:
            redis_handler.add_to_set(key, *slot_names)
        logger.debug('getting slot names of business %s from DB', business.business_name)
        return slot_names
    logger.debug('getting slot names of business %s from cache', business.business_name)
    return redis_handler.get_members_of_set(key)


class RedisNativeHandler:

    def __init__(self):
        self.version = 1

    def add_to_set(self, set_name, *values):
        connection = get_redis_connection('default')
        connection.sadd(self._append_version_prefix(set_name), *values)

    def add_to_sorted_set(self, set_name, *values):
        connection = get_redis_connection('default')
        connection.zadd(self._append_version_prefix(set_name), *values)

    def get_members_of_set(self, set_name):
        connection = get_redis_connection('default')
        return connection.smembers(self._append_version_prefix(set_name))

    def get_first_of_sorted_set(self, sorted_set_name, start, stop):
        connection = get_redis_connection('default')
        return connection.zrevrange(self._append_version_prefix(sorted_set_name), start, stop, withscores=True)

    def increment_score_of_member(self, sorted_set_name, member, incr_by):
        connection = get_redis_connection('default')
        return connection.zincrby(self._append_version_prefix(sorted_set_name), member, amount=incr_by)

    def _append_version_prefix(self, key):
        return ':%s:%s' % (self.version, key)


class LeaderBoardHandler:
    def __init__(self, business):
        self.business = business
        self.redis_handler = RedisNativeHandler()

    def fetch(self):
        key = self.business.get_leaders_cache_key()
        if key not in cache:
            leaders = self.business.get_employees().exclude(role='MA').order_by('-rate')[:5]
            if leaders:
                self.redis_handler.add_to_sorted_set(key, *self._leaders_names_rates_list(leaders))
            logger.debug('Cant find %s leaders in cache; getting them from DB and creating cache leader-board',
                         self.business.business_name)
            return [{'username': e.user.username, 'rate': e.rate} for e in leaders]
        logger.debug('getting leaders of business %s from cache', self.business.business_name)
        leader_list_from_cache = self.redis_handler.get_first_of_sorted_set(key, 0, 4)
        return self._prepare_leader_list(leader_list_from_cache)

    def update_ranks(self, employees, incr_by):
        key = self.business.get_leaders_cache_key()
        for emp in employees:
            self.redis_handler.increment_score_of_member(key, emp.user.username, incr_by)

    @staticmethod
    def _leaders_names_rates_list(leader_emps):
        result = []
        for e in leader_emps:
            result.append(e.rate)
            result.append(e.user.username)
        return result

    @staticmethod
    def _prepare_leader_list(leader_list_from_cache):
        return [{'username': entry[0], 'rate': '%.2f' % entry[1]} for entry in leader_list_from_cache]


class NoLogoFoundError(Exception):
    pass
