import urllib

from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from core.models import ManagerMessage, EmployeeRequest
from core.test.test_helpers import set_employee, create_new_manager, create_new_employee,\
    create_manager_and_employee_groups
from log.test.test_utils import make_data


class EmployeeRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()

    def setUp(self):
        self.incorrect_data = {'incorrect_data': 'incorrect', 'fix_suggestion': 'fix'}
        self.emp_credentials = {'username': 'testuser1', 'password': 'secret'}
        self.manager_credentials = {'username': 'testuser2', 'password': 'secret'}
        create_new_manager(self.manager_credentials)
        create_new_employee(self.emp_credentials)

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


class HandleRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()

    def setUp(self):
        self.emp_credentials = {'username': 'testuser1', 'password': 'secret'}
        self.manager_credentials = {'username': 'testuser2', 'password': 'secret'}
        create_new_manager(self.manager_credentials)
        create_new_employee(self.emp_credentials)

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
        self.client.post('/core/report_incorrect/', data=incorrect_data)


# class BroadcastMessageTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         create_manager_and_employee_groups()
#
#     def setUp(self):
#         self.emp_credentials = {'username': 'testuser1', 'password': 'secret'}
#         self.manager_credentials = {'username': 'testuser2', 'password': 'secret'}
#         create_new_manager(self.manager_credentials)
#         create_new_employee(self.emp_credentials)
#
#     def test_view_url_exists_at_desired_location(self):
#         self.client.login(**self.manager_credentials)
#         resp = self.client.post('/core/handle_emp_request/', data=self.handle_request_data, follow=True)
#         self.assertEqual(resp.status_code, 200)
#
#     def test_view_should_redirect_when_not_logged_in(self):
#         resp = self.client.post('/core/handle_emp_request/', data=self.handle_request_data)
#         self.assertEqual(resp.status_code, 302)
#
#     def test_view_should_redirect_when_employee_is_logged(self):
#         self.client.login(**self.emp_credentials)
#         resp = self.client.post('/core/handle_emp_request/', data=self.handle_request_data)
#         self.assertEqual(resp.status_code, 302)
