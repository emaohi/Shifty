from django.test import TestCase

from core.models import Shift
from core.shift_generator import NaiveShiftGenerator, ThoughtfulShiftGenerator
from core.test.test_helpers import create_slots_for_next_week, create_new_employee
from log.models import Business


class NaiveShiftGeneratorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.waiter = create_new_employee({'username': 'u1', 'password': 'p1'}, 'WA')
        cls.bartender = create_new_employee({'username': 'u2', 'password': 'p2'}, 'BT')
        cls.cook = create_new_employee({'username': 'u3', 'password': 'p3'}, 'CO')
        cls.business = Business.objects.get(business_name='dummy')

    def test_should_generate_successfully_with_only_first_waiter(self):
        another_waiter = create_new_employee({'username': 'u4', 'password': 'p1'}, 'WA')
        num_of_slots = 3
        slots = create_slots_for_next_week(business=self.business, waiter=1, bartender=1, cook=1, num=num_of_slots)
        NaiveShiftGenerator(slots).generate()

        self._assert_num_shifts_created(num_of_slots)
        self.assertEqual(Shift.objects.filter(employees__in=[self.waiter]).count(), num_of_slots)
        self.assertEqual(Shift.objects.filter(employees__in=[another_waiter]).count(), 0)

    def test_should_rollback_in_case_of_failure(self):
        slots = create_slots_for_next_week(business=self.business, waiter=1, bartender=1, cook=1, num=2)
        invalid_slot = create_slots_for_next_week(business=self.business, waiter=1, bartender=2, cook=1, num=1)
        slots.extend(invalid_slot)
        try:
            NaiveShiftGenerator(slots).generate()
        except ValueError:
            pass
        self._assert_num_shifts_created(0)

    def _assert_num_shifts_created(self, num):
        self.assertEqual(Shift.objects.count(), num)


class ThoughtfulShiftGeneratorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.waiter = create_new_employee({'username': 'u1', 'password': 'p1'}, 'WA')
        cls.bartender = create_new_employee({'username': 'u2', 'password': 'p2'}, 'BT')
        cls.cook = create_new_employee({'username': 'u3', 'password': 'p3'}, 'CO')
        cls.business = Business.objects.get(business_name='dummy')

    def test_should_generate_should_prefer_requester_waiter_when_just_one_slot(self):
        num_of_slots = 1
        another_waiter = create_new_employee({'username': 'u4', 'password': 'p1'}, 'WA')
        slots = create_slots_for_next_week(business=self.business, waiter=1, bartender=1, cook=1, num=num_of_slots)
        self._create_slot_request(slot=slots[0], employees=[self.waiter, self.cook, self.bartender, another_waiter])
        ThoughtfulShiftGenerator(slots).generate()

        self.assertEqual(Shift.objects.count(), num_of_slots)
        self.assertTrue(self._emp_has_shift(self.waiter))
        self.assertFalse(self._emp_has_shift(another_waiter))

    def test_should_generate_should_assign_both_waiters_when_just_two_slots(self):
        num_of_slots = 2

        another_waiter = create_new_employee({'username': 'u4', 'password': 'p1'}, 'WA')
        slots = create_slots_for_next_week(business=self.business, waiter=1, bartender=1, cook=1, num=num_of_slots)
        self._create_slot_request(slot=slots[0], employees=[self.waiter, self.cook, self.bartender, another_waiter])

        ThoughtfulShiftGenerator(slots).generate()

        self.assertEqual(Shift.objects.count(), num_of_slots)
        self.assertTrue(self._emp_has_shift(self.waiter))
        self.assertTrue(self._emp_has_shift(another_waiter))

    def test_should_rollback_in_case_of_failure(self):
        slots = create_slots_for_next_week(business=self.business, waiter=1, bartender=1, cook=1, num=2)
        invalid_slot = create_slots_for_next_week(business=self.business, waiter=1, bartender=2, cook=1, num=1)
        slots.extend(invalid_slot)
        try:
            ThoughtfulShiftGenerator(slots).generate()
        except ValueError:
            pass
        self.assertEqual(Shift.objects.count(), 0)

    @staticmethod
    def _emp_has_shift(emp):
        return Shift.objects.filter(employees__in=[emp]).exists()

    def _create_slot_request(self, slot, employees):
        pass
