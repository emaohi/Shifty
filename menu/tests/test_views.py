# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.test.test_helpers import create_manager_and_employee_groups, create_new_manager, create_new_employee
# from menu.tests.test_helpers import create_quiz


class MenuViewsTest(TestCase):
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

    def test_employee_without_quiz_should_get_no_quiz_404(self):
        self.client.login(**self.emp_credentials)
        resp = self.client.get(reverse('menu_test_quiz'))
        self.assertEqual(resp.status_code, 404)

    # def test_employee_with_score_should_get_bad_request(self):
    #     self.client.login(**self.emp_credentials)
    #     emp_user = User.object.get(username=self.emp_credentials['username'])
    #     create_quiz(emp_user)
    #     # submit_quiz(emp_user)
    #     resp = self.client.get(reverse('menu_test_quiz'))
    #     self.assertEqual(resp.status_code, 400)
