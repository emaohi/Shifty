from django.contrib.auth.models import User
from django.test import TestCase

from core.date_utils import get_curr_year, get_next_week_num
from core.models import ShiftSlot
from log.models import Business


class ShiftSlotModelTest(TestCase):

    test_business = None

    @classmethod
    def setUpTestData(cls):
        test_manager = User.objects.create_user({'username': 'testUser', 'password': 'secret'})
        cls.test_business = Business.objects.create(business_name='testBiz', manager=test_manager)
        ShiftSlot.objects.create(business=cls.test_business, year='2016', day='1',
                                 start_hour='12:00:00', end_hour='13:00:00')

    def test_slot_to_string_looks_correctly(self):
        slot = ShiftSlot.objects.get(id=1)
        expected_to_str = 'Shift slot - day: 1, start: 12:00:00, end: 13:00:00'
        self.assertEqual(expected_to_str, str(slot))

    def test_should_return_correct_date_string(self):
        slot = ShiftSlot.objects.get(id=1)
        expected_date_str = '03-01-2016'
        self.assertEqual(expected_date_str, slot.get_date())

    def test_should_fail_if_slot_is_not_next_week(self):
        slot = ShiftSlot.objects.get(id=1)
        self.assertFalse(slot.is_next_week())

    def test_should_succeed_if_slot_is_next_week(self):
        ShiftSlot.objects.create(business=self.test_business, year=get_curr_year(), week=get_next_week_num(),
                                 day='1', start_hour='12:00:00', end_hour='13:00:00')
        slot = ShiftSlot.objects.get(id=2)
        self.assertTrue(slot.is_next_week())
