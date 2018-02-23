import json

from django.test import TestCase

from core.date_utils import __get_days_range_by_week_num
from core.utils import create_constraint_json_from_form


class UtilsTest(TestCase):
    dummy_slot = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '1',
        'num_of_bartenders': '1', 'num_of_cooks': '1'
    }

    def test_constraint_json_should_be_correct_for_data(self):

        expected_json = json.dumps(dict(waiter=dict(num='1', gender=dict(apply_on='1', val='M', op='eq')),
                                        cook=dict(num='1', average=dict(val='2.5', op='gte', apply_on='1')),
                                        bartender=dict(num='1')), sort_keys=True)

        self.dummy_slot['waiter_gender__applyOn_constraint'] = '1'
        self.dummy_slot['waiter_gender__value_constraint'] = 'M'
        self.dummy_slot['waiter_gender__operation_constraint'] = 'eq'

        self.dummy_slot['cook_average_rate__applyOn_constraint'] = '1'
        self.dummy_slot['cook_average_rate__value_constraint'] = '2.5'
        self.dummy_slot['cook_average_rate__operation_constraint'] = 'gte'

        actual_constraint_json = json.dumps(create_constraint_json_from_form(self.dummy_slot), sort_keys=True)

        self.assertEqual(expected_json, actual_constraint_json)

    def test_week_range(self):
        expected_range = ('07/08/2016', '13/08/2016')
        week = 32
        year = '2016'
        actual_day_range = __get_days_range_by_week_num(week, year)

        self.assertEqual(expected_range, actual_day_range)
