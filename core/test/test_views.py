import json
import urllib
from datetime import datetime

from django.test import TestCase, override_settings
from django.urls import reverse
from mock import patch

from core.date_utils import get_days_hours_from_delta
from core.models import EmployeeRequest, ShiftSlot, Shift
from core.test.test_helpers import create_new_manager, create_new_employee, \
    create_manager_and_employee_groups, add_fields_to_slot, set_address_to_business, set_address_to_employee, \
    make_slot_this_in_n_hour_from_now, create_shifts_for_slots
from core.utils import DurationApiClient, RedisNativeHandler
from log.models import EmployeeProfile
patch.object = patch.object


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
class EmployeeRequestViewTest(TestCase):
    incorrect_data = {'incorrect_data': 'incorrect', 'fix_suggestion': 'fix'}
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)

    def setUp(self):

        self.client.logout()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.emp_credentials)
        resp = self.client.post(reverse('report_incorrect'), data=self.incorrect_data)
        self.assertEqual(resp.status_code, 200)

    def test_view_should_redirect_when_not_logged_in(self):
        resp = self.client.post(reverse('report_incorrect'), data=self.incorrect_data, follow=True)
        self.assertRedirects(resp, reverse('login') + '?next=' + urllib.quote(reverse('report_incorrect'), ""))

    def test_view_should_redirect_when_manager_is_logged(self):
        self.client.login(**self.manager_credentials)
        resp = self.client.post(reverse('report_incorrect'), data=self.incorrect_data, follow=True)
        self.assertRedirects(resp, reverse('manager_home') + '?next=' + urllib.quote(reverse('report_incorrect'), ""))


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
class HandleRequestViewTest(TestCase):
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)

    def setUp(self):

        self._create_incorrect_data()
        created_req_id = EmployeeRequest.objects.all().first().id
        self.handle_request_data = {'emp_request_id': str(created_req_id), 'new_status': 'A'}

        self.client.logout()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.manager_credentials)
        resp = self.client.post(reverse('handle_emp_request'), data=self.handle_request_data)
        self.assertEqual(resp.status_code, 200)

    def test_view_should_redirect_when_not_logged_in(self):
        resp = self.client.post(reverse('handle_emp_request'), data=self.handle_request_data, follow=True)
        self.assertRedirects(resp, reverse('login') + '?next=' + urllib.quote(reverse('handle_emp_request'), ""))

    def test_view_should_redirect_when_employee_is_logged(self):
        self.client.login(**self.emp_credentials)
        resp = self.client.post(reverse('handle_emp_request'), data=self.handle_request_data, follow=True)
        self.assertRedirects(resp, reverse('emp_home') + '?next=' + urllib.quote(reverse('handle_emp_request'), ""))

    def _create_incorrect_data(self):
        self.client.login(**self.emp_credentials)
        incorrect_data = {'incorrect_data': 'incorrect', 'fix_suggestion': 'fix'}
        self.client.post(reverse('report_incorrect'), data=incorrect_data)


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
class BroadcastMessageViewTest(TestCase):
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()

        cls.broadcast_msg = {'subject': 'broadcast_subject', 'text': 'broadcast_text'}
        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)

    def setUp(self):

        self.client.logout()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.manager_credentials)
        resp = self.client.post(reverse('broadcast_msg'), data=self.broadcast_msg, follow=True)
        self.assertEqual(str(resp.context['user']), self.manager_credentials['username'])
        self.assertEqual(resp.status_code, 200)

    def test_initial_form_exist(self):
        self.client.login(**self.manager_credentials)
        resp = self.client.get(reverse('broadcast_msg'))
        self.assertEqual(str(resp.context['user']), self.manager_credentials['username'])
        self.assertTrue('form' in resp.context)

    def test_view_should_redirect_when_not_logged_in(self):
        resp = self.client.post(reverse('broadcast_msg'), data=self.broadcast_msg, follow=True)
        self.assertRedirects(resp, reverse('login') + '?next=' + urllib.quote(reverse('broadcast_msg'), ""))

    def test_view_should_redirect_when_employee_is_logged(self):
        self.client.login(**self.emp_credentials)
        resp = self.client.post(reverse('broadcast_msg'), data=self.broadcast_msg, follow=True)
        self.assertRedirects(resp, reverse('emp_home') + '?next=' + urllib.quote(reverse('broadcast_msg'), ""))


# pylint: disable=unused-argument
@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
@patch.object(RedisNativeHandler, 'add_to_set')
class AddShiftSlotViewTest(TestCase):
    dummy_slot = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '0',
        'num_of_bartenders': '0', 'num_of_cooks': '0'
    }
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()

        add_fields_to_slot(cls.dummy_slot)
        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)

    def setUp(self):

        self.client.logout()

    def test_view_url_exists_at_desired_location(self, mocked):
        self.client.login(**self.manager_credentials)
        resp = self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        self.assertEqual(str(resp.context['user']), self.manager_credentials['username'])
        self.assertEqual(resp.status_code, 200)

    def test_initial_form_exist_and_contain_initial_day_and_start_hour(self, mocked):
        self.client.login(**self.manager_credentials)

        test_day = '2'
        test_start_time = '06-00-00'

        resp = self.client.get(reverse('add_shift_slot') + '?day=%s&startTime=%s' % (test_day, test_start_time))
        self.assertEqual(str(resp.context['user']), self.manager_credentials['username'])
        self.assertTrue('form' in resp.context)
        self.assertEqual(resp.context['form'].initial['day'], test_day)
        self.assertEqual(resp.context['form'].initial['start_hour'], test_start_time.replace('-', ':'))

    def test_view_should_redirect_when_not_logged_in(self, mocked):
        resp = self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        self.assertRedirects(resp, reverse('login') + '?next=' + urllib.quote(reverse('add_shift_slot'), ""))

    def test_view_should_redirect_when_employee_is_logged(self, mocked):
        self.client.login(**self.emp_credentials)
        resp = self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        self.assertRedirects(resp, reverse('emp_home') + '?next=' + urllib.quote(reverse('add_shift_slot'), ""))


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
class DeleteShiftSlotViewTest(TestCase):
    dummy_slot = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '0',
        'num_of_bartenders': '0', 'num_of_cooks': '0'
    }
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)
        add_fields_to_slot(cls.dummy_slot)

    def setUp(self):

        self.client.login(**self.manager_credentials)
        with patch.object(RedisNativeHandler, 'add_to_set'):
            self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        self.client.logout()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.manager_credentials)
        slot_id = ShiftSlot.objects.get(day=self.dummy_slot['day']).id
        resp = self.client.post(reverse('delete_shift_slot'), data={'slot_id': slot_id}, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_view_should_reply_bad_request_on_get(self):
        self.client.login(**self.manager_credentials)
        resp = self.client.get(reverse('delete_shift_slot'), follow=True)
        self.assertEqual(resp.status_code, 400)

    def test_view_should_redirect_when_not_logged_in(self):
        resp = self.client.post(reverse('delete_shift_slot'), data=self.dummy_slot, follow=True)
        self.assertRedirects(resp, reverse('login') + '?next=' + urllib.quote(reverse('delete_shift_slot'), ""))

    def test_view_should_redirect_when_employee_is_logged(self):
        self.client.login(**self.emp_credentials)
        resp = self.client.post(reverse('delete_shift_slot'), data=self.dummy_slot, follow=True)
        self.assertRedirects(resp, reverse('emp_home') + '?next=' + urllib.quote(reverse('delete_shift_slot'), ""))


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class GetDurationDataViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()

    def setUp(self):
        self.manager_credentials = {'username': 'testuser2', 'password': 'secret'}
        create_new_manager(self.manager_credentials)
        set_address_to_business(username=self.manager_credentials['username'], address='Tel-Aviv')

    @patch.object(DurationApiClient, 'get_dist_data')
    def test_view_should_succeed(self, mock_func):

        mock_func.return_value = {'driving': '1', 'walking': '2'}

        set_address_to_employee(username=self.manager_credentials['username'], address='Haifa')
        self.client.login(**self.manager_credentials)
        resp = self.client.get(reverse('duration_data'), {'walking': 'True', 'driving': 'True'})
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {'driving': '1',
                                            'walking': '2'})

    def test_view_should_bad_request_when_no_emp_address(self):
        self.client.login(**self.manager_credentials)
        resp = self.client.get(reverse('duration_data'), {'walking': 'True', 'driving': 'True'})
        self.assertEqual(resp.status_code, 400)

    def test_view_should_bad_request_when_not_valid_emp_address(self):
        set_address_to_employee(username=self.manager_credentials['username'], address='Blabla')
        self.client.login(**self.manager_credentials)
        resp = self.client.get(reverse('duration_data'), {'walking': 'True', 'driving': 'True'})
        self.assertEqual(resp.status_code, 400)


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
class GetNextShiftTimer(TestCase):
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}
    dummy_slot = {
        'day': '1', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '1',
        'num_of_bartenders': '0', 'num_of_cooks': '0'
    }

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)
        add_fields_to_slot(cls.dummy_slot)

    def setUp(self):
        with patch.object(RedisNativeHandler, 'add_to_set'):
            self.client.login(**self.manager_credentials)
            self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)

    def test_view_should_succeed_when_one_slot(self):
        self._create_upcoming_shifts_for_existing_slots(1)

        self.client.login(**self.emp_credentials)
        resp = self.client.get(reverse('time_to_next_shift'))
        self.assertEqual(resp.status_code, 200)
        days, hours = get_days_hours_from_delta(ShiftSlot.objects.first().get_datetime() - datetime.now())
        self.assertEqual(resp.content, '%s days, %s hours' % (days, hours))

    def test_view_should_choose_earliest_when_two_slots(self):
        second_slot = {k: v for k, v in self.dummy_slot.items()}
        second_slot['day'] = '2'
        with patch.object(RedisNativeHandler, 'add_to_set'):
            self.client.post(reverse('add_shift_slot'), data=second_slot, follow=True)

        self._create_upcoming_shifts_for_existing_slots(2)

        self.client.login(**self.emp_credentials)
        resp = self.client.get(reverse('time_to_next_shift'))
        self.assertEqual(resp.status_code, 200)
        days, hours = get_days_hours_from_delta(ShiftSlot.objects.first().get_datetime() - datetime.now())
        self.assertEqual(resp.content, '%s days, %s hours' % (days, hours))

    def _create_upcoming_shifts_for_existing_slots(self, num):
        slots = ShiftSlot.objects.all()[:num]
        for num_hours, slot in enumerate(slots):
            make_slot_this_in_n_hour_from_now(slot, num_hours + 1)
        create_shifts_for_slots(slots, emps=EmployeeProfile.objects.filter(
            user__username=self.emp_credentials['username']))


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
class GetSlotRequestersViewTest(TestCase):
    dummy_slot = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '1',
        'num_of_bartenders': '0', 'num_of_cooks': '0'
    }
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        add_fields_to_slot(cls.dummy_slot)

        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)

    def setUp(self):
        self.client.login(**self.manager_credentials)
        with patch.object(RedisNativeHandler, 'add_to_set'):
            self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        self.client.post(reverse('finish_slots'), {'isFinished': 'true'})
        self.client.logout()

        self.client.login(**self.emp_credentials)
        slot_id = str(ShiftSlot.objects.first().id)
        self.client.post(reverse('slots_request'), data={'requested_slots': [slot_id]}, follow=True)
        self.client.logout()

    def test_view_should_succeed(self):
        self.client.login(**self.manager_credentials)
        slot_id = str(ShiftSlot.objects.first().id)
        resp = self.client.get(reverse('slot_request_employees', kwargs={'slot_id': slot_id}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['emps'][0].user.username, 'testuser1')


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
class GenerateShiftsViewTest(TestCase):
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}
    dummy_slot = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '1',
        'num_of_bartenders': '0', 'num_of_cooks': '0'
    }

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)
        add_fields_to_slot(cls.dummy_slot)

    def test_view_should_return_bad_request_if_no_slots(self):
        self.client.login(**self.manager_credentials)
        resp = self.client.post(reverse('generate_shifts'))
        self.assertEqual(resp.status_code, 400)

    def test_should_succeed_if_slot_exist(self):
        self.client.login(**self.manager_credentials)
        with patch.object(RedisNativeHandler, 'add_to_set'):
            self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        resp = self.client.post(reverse('generate_shifts'))
        self.assertEqual(resp.status_code, 200)

        self.assertTrue(Shift.objects.exists())


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}, CELERY=False)
class GetLogoUrlViewTest(TestCase):
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        create_new_manager(cls.manager_credentials)

    def setUp(self):
        self.client.login(**self.manager_credentials)

    def test_should_get_url(self):
        restaurant = 'japanika'
        res = self.client.get(reverse('logo_suggestion') + '?name=%s' % restaurant)
        json.loads(res.content).get('logo_url')
        self.assertEqual(res.status_code, 200)

    def test_should_raise_no_logo_found_error(self):
        restaurant = 'blabla'
        res = self.client.get(reverse('logo_suggestion') + '?name=%s' % restaurant)
        self.assertEqual(res.status_code, 400)
