import urllib

from django.test import TestCase, override_settings
from django.urls import reverse
from mock import patch

from core.models import EmployeeRequest, ShiftSlot, Shift
from core.test.test_helpers import create_new_manager, create_new_employee, \
    create_manager_and_employee_groups, add_fields_to_slot, set_address_to_business, set_address_to_employee


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

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.manager_credentials)
        resp = self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        self.assertEqual(str(resp.context['user']), self.manager_credentials['username'])
        self.assertEqual(resp.status_code, 200)

    def test_initial_form_exist_and_contain_initial_day_and_start_hour(self):
        self.client.login(**self.manager_credentials)

        test_day = '2'
        test_start_time = '06-00-00'

        resp = self.client.get(reverse('add_shift_slot') + '?day=%s&startTime=%s' % (test_day, test_start_time))
        self.assertEqual(str(resp.context['user']), self.manager_credentials['username'])
        self.assertTrue('form' in resp.context)
        self.assertEqual(resp.context['form'].initial['day'], test_day)
        self.assertEqual(resp.context['form'].initial['start_hour'], test_start_time.replace('-', ':'))

    def test_view_should_redirect_when_not_logged_in(self):
        resp = self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        self.assertRedirects(resp, reverse('login') + '?next=' + urllib.quote(reverse('add_shift_slot'), ""))

    def test_view_should_redirect_when_employee_is_logged(self):
        self.client.login(**self.emp_credentials)
        resp = self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        self.assertRedirects(resp, reverse('emp_home') + '?next=' + urllib.quote(reverse('add_shift_slot'), ""))


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

    @patch('core.views.parse_duration_data')
    def test_view_should_succeed(self, mock_func):

        mock_func.return_value = ('1', '2')

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


@override_settings(CELERY=False)
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
        self.client.post(reverse('add_shift_slot'), data=self.dummy_slot, follow=True)
        resp = self.client.post(reverse('generate_shifts'))
        self.assertEqual(resp.status_code, 200)

        self.assertTrue(Shift.objects.exists())
