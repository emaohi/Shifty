import datetime

from django.test import TestCase

from core.date_utils import get_next_week_num
from core.forms import ShiftSlotForm
from core.models import ShiftSlot
from core.test.test_helpers import create_new_employee, create_manager_and_employee_groups
from log.models import Business, EmployeeProfile


class ShiftSlotFormTest(TestCase):
    dummy_slot = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '1',
        'num_of_bartenders': '1', 'num_of_cooks': '1'
    }

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()

    def setUp(self):
        for role in ['waiter', 'bartender', 'cook']:
            for field in ['gender', 'age', 'average_rate', 'months_working']:
                self.dummy_slot[role + '_' + field + '__value_constraint'] = ''
                self.dummy_slot[role + '_' + field + '__applyOn_constraint'] = ''
                self.dummy_slot[role + '_' + field + '__operation_constraint'] = ''
        self.emp_credentials = {'username': 'testuser1', 'password': 'secret'}
        create_new_employee(self.emp_credentials)
        test_emp = EmployeeProfile.objects.get(user__username=self.emp_credentials['username'])
        test_emp.gender = 'M'
        test_emp.role = 'WA'
        test_emp.birth_date = datetime.date(1994, 1, 1)
        test_emp.save()

    def test_no_constraints_should_be_valid(self):
        form = ShiftSlotForm(self.dummy_slot, business=Business.objects.get(business_name='dummy'))
        if not form.is_valid():
            print form.errors
        self.assertTrue(form.is_valid())

    def test_enough_males_should_success(self):
        lookup = 'waiter_gender'
        self.dummy_slot[lookup + '__operation_constraint'] = 'eq'
        self.dummy_slot[lookup + '__value_constraint'] = 'M'
        self.dummy_slot[lookup + '__applyOn_constraint'] = '1'

        form = ShiftSlotForm(self.dummy_slot, business=Business.objects.get(business_name='dummy'))
        self.assertTrue(form.is_valid())

    def test_not_enough_females_should_fail(self):
        lookup = 'waiter_gender'
        self.dummy_slot[lookup + '__operation_constraint'] = 'eq'
        self.dummy_slot[lookup + '__value_constraint'] = 'F'
        self.dummy_slot[lookup + '__applyOn_constraint'] = '1'

        form = ShiftSlotForm(self.dummy_slot, business=Business.objects.get(business_name='dummy'))
        self.assertFalse(form.is_valid())

    def test_not_enough_old_emps_should_fail(self):
        lookup = 'waiter_age'
        self.dummy_slot[lookup + '__operation_constraint'] = 'gte'
        self.dummy_slot[lookup + '__value_constraint'] = '28'
        self.dummy_slot[lookup + '__applyOn_constraint'] = '1'

        form = ShiftSlotForm(self.dummy_slot, business=Business.objects.get(business_name='dummy'))
        self.assertFalse(form.is_valid())

    def test_overlap_slots_should_fail(self):
        ShiftSlot.objects.create(business=Business.objects.get(business_name='dummy'), week=get_next_week_num(),
                                 day='3', start_hour='12:00:00', end_hour='13:00:00')
        form = ShiftSlotForm(self.dummy_slot, business=Business.objects.get(business_name='dummy'))
        self.assertFalse(form.is_valid())
