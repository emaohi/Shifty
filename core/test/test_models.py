from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.signals import m2m_changed, post_save
from django.test import TestCase, override_settings
from mock import patch

from Shifty.utils import get_time_from_str
from core.date_utils import get_curr_year, get_next_week_num
from core.models import ShiftSlot, Shift, ShiftSwap, EmployeeRequest, ManagerMessage, SavedSlot
from core.test.test_helpers import create_new_manager, create_new_employee, create_manager_and_employee_groups, \
    create_multiple_employees, CatchSignal
from core.utils import RedisNativeHandler
from log.models import Business, EmployeeProfile
patch.object = patch.object


class EmployeeRequestModelTest(TestCase):
    emp1_credentials = {'username': 'testuser1', 'password': 'secret'}
    emp2_credentials = {'username': 'testuser2', 'password': 'secret'}
    emp_request = None

    @classmethod
    def setUpTestData(cls):
        create_manager_and_employee_groups()
        create_new_employee(cls.emp1_credentials)
        create_new_employee(cls.emp2_credentials)

    def test_title_and_text_should_be_configured_if_not_set(self):
        self.emp_request = EmployeeRequest.objects.create()
        self.assertTrue(self.emp_request.subject == 'Other subject')
        self.assertTrue(self.emp_request.text == 'Other text')

    def test_title_and_text_should_be_overridden_if_set(self):
        self.emp_request = EmployeeRequest.objects.create(subject='Some subject', text='Some text')
        self.assertTrue(self.emp_request.subject == 'Some subject')
        self.assertTrue(self.emp_request.text == 'Some text')


class ManagerMessageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.employees = create_multiple_employees(6)
        cls.manager_message = ManagerMessage.objects.create(business=Business.objects.first(),
                                                            subject='bla', text='bla')

    def test_should_create_correct_recipients_string_when_less_than_5(self):
        self.manager_message.recipients.set(self.employees[:3])
        self.assertEqual(self.manager_message.get_recipients_string(), 'test_user_0, test_user_1, test_user_2')

    def test_should_create_correct_recipients_string_when_more_than_5(self):
        self.manager_message.recipients.set(self.employees)
        self.assertEqual(self.manager_message.get_recipients_string(), 'test_user_0, test_user_1, test_user_2,'
                                                                       ' test_user_3, test_user_4 and 1 more')

    def test_manager_message_should_increment_new_msgs_of_emps(self):
        first_emp = self.employees[0]
        self.assertEqual(first_emp.new_messages, 0)
        self.manager_message.recipients.set(self.employees[:1])
        first_emp.refresh_from_db()
        self.assertEqual(first_emp.new_messages, 1)


class ShiftSlotModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_manager = User.objects.create_user({'username': 'testUser', 'password': 'secret'})
        cls.test_business = Business.objects.create(business_name='testBiz', manager=test_manager)
        cls.slot = ShiftSlot.objects.create(business=cls.test_business, year='2016', day='1',
                                            start_hour='12:00:00', end_hour='13:00:00')

    def setUp(self):
        self.slot = ShiftSlot.objects.get(year='2016')

    def test_slot_to_string_looks_correctly(self):
        expected_to_str = 'Custom slot(#%s) - Sunday, 03-01-2016, 12:00 to 13:00:00' % self.slot.id
        self.assertEqual(expected_to_str, str(self.slot))

    def test_should_return_correct_date_string(self):
        expected_date_str = '03-01-2016'
        self.assertEqual(expected_date_str, self.slot.get_date())

    def test_should_not_be_next_week(self):
        self.assertFalse(self.slot.is_next_week())

    def test_should_be_next_week(self):
        slot = ShiftSlot.objects.create(business=self.test_business, year=get_curr_year(), week=get_next_week_num(),
                                        day='1', start_hour='12:30:00', end_hour='13:00:00')
        self.assertTrue(slot.is_next_week())

    def test_name_should_be_custom_if_not_set(self):
        self.assertEqual(self.slot.name, 'Custom')

    def test_update_slot_with_different_saved_slot_should_raise_integrity_error(self):
        self.slot.saved_slot = SavedSlot.objects.create(name='test_saved_slot', constraints='{}')
        self.assertRaises(IntegrityError, self.slot.save)

    def test_attributes_should_be_copied_from_saved_slot(self):
        saved_slot = SavedSlot.objects.create(name='test_saved_slot', constraints='{}')
        slot = ShiftSlot.objects.create(business=self.test_business, year=get_curr_year(), week=get_next_week_num(),
                                        day='1', start_hour='12:30:00', end_hour='13:00:00', saved_slot=saved_slot)
        self.assertEqual(slot.name, saved_slot.name)
        self.assertEqual(slot.constraints, saved_slot.constraints)
        self.assertEqual(slot.is_mandatory, saved_slot.is_mandatory)

    def test_slot_should_output_correct_time_frame(self):
        self.assertEqual(self.slot.get_time_frame_code(), 1)
        self.slot.day = 3
        self.slot.start_hour = get_time_from_str('16:00')
        self.slot.save()
        self.assertEqual(self.slot.get_time_frame_code(), 6)


@override_settings(CACHES={'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "redis://127.0.0.1:6379/2"}})
class ShiftModelTest(TestCase):

    first_emp_credentials = {'username': 'testUser1', 'password': 'secret1'}
    second_emp_credentials = {'username': 'testUser2', 'password': 'secret2'}

    @classmethod
    def setUpTestData(cls):
        create_new_manager({'username': 'testUser', 'password': 'secret'})
        cls.test_business = Business.objects.create(business_name='testBiz')
        cls.emp = create_new_employee(cls.first_emp_credentials)
        cls.other_emp = create_new_employee(cls.second_emp_credentials)
        cls.first_slot = ShiftSlot.objects.create(business=cls.test_business, day='1',
                                                  start_hour='12:00:00', end_hour='13:00:00', constraints='{}')
        cls.second_slot = ShiftSlot.objects.create(business=cls.test_business, day='1',
                                                   start_hour='16:00:00', end_hour='18:00:00', constraints='{}')

    def setUp(self):
        self.first_shift, self.second_shift = self._create_shifts()

    def test_emp_rate_should_be_updated_correctly(self):
        self.first_shift.rank = 3
        self.first_shift.save()
        self.emp.refresh_from_db()
        self.assertEqual(self.emp.rate, 3)

        self.second_shift.rank = 3
        self.second_shift.save()
        self.emp.refresh_from_db()
        self.assertEqual(self.emp.rate, 4.5)

    def _create_shifts(self):
        first_shift = Shift.objects.create(slot=self.first_slot)
        first_shift.employees.add(self.emp)
        second_shift = Shift.objects.create(slot=self.second_slot)
        second_shift.employees.add(self.emp)
        second_shift.employees.add(self.other_emp)
        return first_shift, second_shift


class ShiftSwapModelTest(TestCase):

    first_emp_credentials = {'username': 'testUser1', 'password': 'secret1'}
    second_emp_credentials = {'username': 'testUser2', 'password': 'secret2'}

    @classmethod
    def setUpTestData(cls):
        create_new_manager({'username': 'testUser', 'password': 'secret'})
        cls.test_business = Business.objects.create(business_name='testBiz')
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
            for _ in range(2):
                ShiftSwap.objects.create(requester=first_emp, responder=second_emp,
                                         requested_shift=self.first_shift, requester_shift=self.second_shift)

    def test_should_swap_employees(self):
        self._create_swap_request(2)
        first_emp, second_emp = self._get_emps()

        self.assertTrue(first_emp in self.second_shift.employees.all() and
                        second_emp in self.first_shift.employees.all())

    def test_should_create_employee_request(self):
        self._create_swap_request(1)
        first_emp, _ = self._get_emps()

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


class SignalModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_business = Business.objects.create(business_name='testBiz')
        create_new_employee({'username': 'testUser1', 'password': 'secret1'})
        cls.first_slot = ShiftSlot.objects.create(business=cls.test_business, day='1',
                                                  start_hour='12:00:00', end_hour='13:00:00', constraints='{}')

    def setUp(self):
        self.manager_message = ManagerMessage.objects.create(business=self.test_business, subject='s', text='t')

    def test_should_catch_m2m_changed_signal_when_adding_recipients(self):
        with CatchSignal(m2m_changed) as handler:
            self.manager_message.recipients.add(EmployeeProfile.objects.first())
        handler.assert_called()

    def test_should_not_catch_m2m_changed_signal_when_no_adding_recipients(self):
        with CatchSignal(m2m_changed) as handler:
            self.manager_message.text = 'another'
        handler.assert_not_called()

    def test_should_catch_post_save(self):
        with CatchSignal(post_save) as handler:
            Shift.objects.create(slot=self.first_slot)
        handler.assert_called()
