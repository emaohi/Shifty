import json

from django.test import TestCase

from core.utils import SlotConstraintCreator


class ConstraintCreatorTest(TestCase):
    dummy_slot = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '1',
        'num_of_bartenders': '1', 'num_of_cooks': '1'
    }

    @classmethod
    def setUpTestData(cls):

    def test_constraint_json_should_be_correct_for_data(self):

        expected_json = json.dumps(dict(waiter=dict(num='1', gender=dict(apply_on='1', val='M', op='eq')),
                                        cook=dict(num='1', average=dict(val='2.5', op='gte', apply_on='1')),
                                        bartender=dict(num='1')), sort_keys=True)

        self._add_fields_to_slot()

        actual_constraint_json = json.dumps(SlotConstraintCreator(self.dummy_slot).create(),
                                            sort_keys=True)

        self.assertEqual(expected_json, actual_constraint_json)

    def _add_fields_to_slot(self):
        self.dummy_slot['waiter_gender__applyOn_constraint'] = '1'
        self.dummy_slot['waiter_gender__value_constraint'] = 'M'
        self.dummy_slot['waiter_gender__operation_constraint'] = 'eq'
        self.dummy_slot['cook_average_rate__applyOn_constraint'] = '1'
        self.dummy_slot['cook_average_rate__value_constraint'] = '2.5'
        self.dummy_slot['cook_average_rate__operation_constraint'] = 'gte'
