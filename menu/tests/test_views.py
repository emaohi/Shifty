# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.test.test_helpers import create_manager_and_employee_groups, create_new_manager, create_new_employee
from menu.tests.test_helpers import create_quiz, get_quiz_submission_data


class MenuViewsTest(TestCase):
    incorrect_data = {'incorrect_data': 'incorrect', 'fix_suggestion': 'fix'}
    emp_credentials = {'username': 'testuser1', 'password': 'secret'}
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        create_new_manager(cls.manager_credentials)
        create_new_employee(cls.emp_credentials)

        create_quiz(User.objects.get(username=cls.emp_credentials['username']))

    def setUp(self):
        self.client.logout()

    def test_cook_employee_without_quiz_should_get_no_quiz_404(self):
        self.client.login(**self.emp_credentials)
        self._change_role_to('CO')
        resp = self.client.get(reverse('menu_test_quiz'))
        self.assertEqual(resp.status_code, 404)

    def _change_role_to(self, role):
        emp_profile = User.objects.get(username=self.emp_credentials['username']).profile
        emp_profile.role = role
        emp_profile.save()

    def test_employee_with_score_should_get_bad_request(self):
        self.client.login(**self.emp_credentials)

        self._submit_not_answered_quiz()

        resp = self.client.get(reverse('menu_test_quiz'))
        self.assertEqual(resp.status_code, 400)

    def test_employee_should_get_100_for_correct_question(self):
        self.client.login(**self.emp_credentials)

        resp = self._submit_correct_quiz()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content)['score'], 100)

    def test_retry_request_should_respond_ok(self):
        self.client.login(**self.emp_credentials)

        resp = self._submit_retry_request()
        self.assertEqual(resp.status_code, 200)

    def test_retry_request_should_respond_BadRequest(self):
        self.client.login(**self.emp_credentials)

        self._submit_retry_request()

        resp = self._submit_retry_request()
        self.assertEqual(resp.status_code, 400)

    def _submit_correct_quiz(self):
        quiz_submission_data = get_quiz_submission_data()
        json_data = json.loads(quiz_submission_data)
        json_data['questions'][0]['answers'][0]['selected'] = True
        return self.client.post(reverse('quiz_submission'), data=json.dumps(json_data), follow=True,
                                content_type='application/json')

    def _submit_not_answered_quiz(self):
        quiz_submission_data = get_quiz_submission_data()
        self.client.post(reverse('quiz_submission'), data=quiz_submission_data, follow=True,
                         content_type='application/json')

    def _submit_retry_request(self):
        return self.client.post(reverse('ask_retry'), data='{}', follow=True, content_type='application/json')
