from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from core.date_utils import get_curr_year, get_next_week_num
from core.models import ShiftSlot, Shift, ShiftSwap, EmployeeRequest
from core.test.test_helpers import create_new_manager, create_new_employee
from log.models import Business, EmployeeProfile


class ShiftSlotModelTest(TestCase):
    test_business = None

    slot = None

    @classmethod
    def setUpTestData(cls):
        test_manager = User.objects.create_user({'username': 'testUser', 'password': 'secret'})
        cls.test_business = Business.objects.create(business_name='testBiz', manager=test_manager)
        cls.slot = ShiftSlot.objects.create(business=cls.test_business, year='2016', day='1',
                                            start_hour='12:00:00', end_hour='13:00:00')

    def test_slot_to_string_looks_correctly(self):
        slot = ShiftSlot.objects.get(year='2016')
        expected_to_str = 'Custom slot(#%s) - Sunday, 12:00:00 to 13:00:00' % self.slot.id
        self.assertEqual(expected_to_str, str(slot))

    def test_should_return_correct_date_string(self):
        slot = ShiftSlot.objects.get(year='2016')
        expected_date_str = '03-01-2016'
        self.assertEqual(expected_date_str, slot.get_date())

    def test_should_fail_if_slot_is_not_next_week(self):
        slot = ShiftSlot.objects.get(year='2016')
        self.assertFalse(slot.is_next_week())

    def test_should_succeed_if_slot_is_next_week(self):
        ShiftSlot.objects.create(business=self.test_business, year=get_curr_year(), week=get_next_week_num(),
                                 day='1', start_hour='12:30:00', end_hour='13:00:00')
        slot = ShiftSlot.objects.get(start_hour='12:30:00')
        self.assertTrue(slot.is_next_week())


class ShiftSwapModelTest(TestCase):

    first_emp_credentials = {'username': 'testUser1', 'password': 'secret1'}
    second_emp_credentials = {'username': 'testUser2', 'password': 'secret2'}

    @classmethod
    def setUpTestData(cls):
        test_manager = create_new_manager({'username': 'testUser', 'password': 'secret'})
        cls.test_business = Business.objects.create(business_name='testBiz', manager=test_manager)
        create_new_employee(cls.first_emp_credentials)
        create_new_employee(cls.second_emp_credentials)
        cls.first_slot = ShiftSlot.objects.create(business=cls.test_business, day='1',
                                                  start_hour='12:00:00', end_hour='13:00:00', constraints='{}')
        cls.second_slot = ShiftSlot.objects.create(business=cls.test_business, day='1',
                                                   start_hour='16:00:00', end_hour='18:00:00', constraints='{}')

    def setUp(self):
        self.first_shift, self.second_shift = self._create_shifts()

    def test_should_raise_integrity_error_when_unique_conditions_are_broken(self):
        with self.assertRaises(IntegrityError):
            first_emp, second_emp = self._get_emps()
            for i in range(2):
                ShiftSwap.objects.create(requester=first_emp, responder=second_emp,
                                         requested_shift=self.first_shift, requester_shift=self.second_shift)

    def test_should_swap_employees(self):
        self._create_swap_request(2)
        first_emp, second_emp = self._get_emps()

        self.assertTrue(first_emp in self.second_shift.employees.all() and
                        second_emp in self.first_shift.employees.all())

    def test_should_create_employee_request(self):
        self._create_swap_request(1)
        first_emp, second_emp = self._get_emps()

        self.assertTrue(EmployeeRequest.objects.filter(issuers__in=[first_emp]).exists())

    def _create_swap_request(self, accept_step):
        first_emp, second_emp = self._get_emps()
        swap_request = ShiftSwap.objects.create(requester=first_emp, responder=second_emp,
                                                requester_shift=self.first_shift, requested_shift=self.second_shift)
        swap_request.accept_step = accept_step
        swap_request.save()

    def _create_shifts(self):
        first_shift = Shift.objects.create(slot=self.first_slot)
        first_shift.employees.add(self._get_emps()[0])
        second_shift = Shift.objects.create(slot=self.second_slot)
        second_shift.employees.add(self._get_emps()[1])

        return first_shift, second_shift

    def _get_emps(self):
        first_emp = EmployeeProfile.objects.get(user__username=self.first_emp_credentials['username'])
        second_emp = EmployeeProfile.objects.get(user__username=self.second_emp_credentials['username'])
        return first_emp, second_emp
