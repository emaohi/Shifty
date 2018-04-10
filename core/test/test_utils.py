import json

from django.conf import settings
from django.test import TestCase

from core.models import ShiftSlot
from core.test.test_helpers import add_fields_to_slot, get_business_of_username, create_new_manager
from core.utils import SlotConstraintCreator, LanguageValidator, SlotCreator


class ConstraintCreatorTest(TestCase):
    dummy_slot = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '1',
        'num_of_bartenders': '1', 'num_of_cooks': '1'
    }

    @classmethod
    def setUpTestData(cls):
        cls._add_fields_to_slot()

    @classmethod
    def _add_fields_to_slot(cls):
        cls.dummy_slot['waiter_gender__applyOn_constraint'] = '1'
        cls.dummy_slot['waiter_gender__value_constraint'] = 'M'
        cls.dummy_slot['waiter_gender__operation_constraint'] = 'eq'
        cls.dummy_slot['cook_average_rate__applyOn_constraint'] = '1'
        cls.dummy_slot['cook_average_rate__value_constraint'] = '2.5'
        cls.dummy_slot['cook_average_rate__operation_constraint'] = 'gte'

    def test_constraint_json_should_be_correct_for_data(self):
        expected_json = json.dumps(dict(waiter=dict(num='1', gender=dict(apply_on='1', val='M', op='eq')),
                                        cook=dict(num='1', average=dict(val='2.5', op='gte', apply_on='1')),
                                        bartender=dict(num='1')), sort_keys=True)
        constraints = SlotConstraintCreator(self.dummy_slot).create()

        self.assertEqual(expected_json, json.dumps(constraints, sort_keys=True))


class LanguageValidatorTest(TestCase):

    validator = LanguageValidator(settings.PROFANITY_SERVICE_URL)
    PROFANITY_WORD = 'FUCK'
    NON_PROFANITY_WORD = 'bla'

    def test_should_respond_with_non_valid_finding(self):
        self.assertFalse(self.validator.validate(self.PROFANITY_WORD))

    def test_should_respond_with_valid_finding(self):
        self.assertTrue(self.validator.validate(self.NON_PROFANITY_WORD))


class SlotCreatorTest(TestCase):
    dummy_slot_data = {
        'day': '3', 'start_hour': '12:00:00', 'end_hour': '14:00:00', 'num_of_waiters': '0',
        'num_of_bartenders': '0', 'num_of_cooks': '0', 'name': '', 'save_as': '', 'mandatory': False
    }
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}

    @classmethod
    def setUpTestData(cls):
        create_new_manager(cls.manager_credentials)
        add_fields_to_slot(cls.dummy_slot_data)

    def test_should_create_new_custom_slot(self):
        manager_business = get_business_of_username(username=self.manager_credentials['username'])
        constraint_creator = SlotConstraintCreator(self.dummy_slot_data)
        creator = SlotCreator(business=manager_business, slot_data=self.dummy_slot_data,
                              constraint_creator=constraint_creator)

        creator.create()

        self.assertTrue(ShiftSlot.objects.filter(name='Custom').exists())

    def test_should_create_new_named_slot_with_saved_slot(self):
        pass

    def test_should_create_slot_from_existing_saved_slot(self):
        pass
