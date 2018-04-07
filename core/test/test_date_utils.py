from django.test import TestCase

from core.date_utils import get_days_range_by_week_num


class DateUtilsTest(TestCase):

    def test_week_range(self):
        expected_range = ('07/08/2016', '13/08/2016')
        week = 32
        year = '2016'
        actual_day_range = get_days_range_by_week_num(week, year)

        self.assertEqual(expected_range, actual_day_range)
