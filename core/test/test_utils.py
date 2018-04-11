import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase

from core.models import ShiftSlot, SavedSlot
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
        'num_of_bartenders': '0', 'num_of_cooks': '0', 'mandatory': False
    }
    manager_credentials = {'username': 'testuser2', 'password': 'secret'}
    manager_business = None

    @classmethod
    def setUpTestData(cls):
        create_new_manager(cls.manager_credentials)
        add_fields_to_slot(cls.dummy_slot_data)
        cls.manager_business = get_business_of_username(username=cls.manager_credentials['username'])

    def test_should_create_new_custom_slot(self):
        self._set_name_and_save_as(name_val='', save_as_val='')
        constraint_creator = SlotConstraintCreator(self.dummy_slot_data)
        creator = SlotCreator(business=self.manager_business, slot_data=self.dummy_slot_data,
                              constraint_creator=constraint_creator)

        creator.create()

        self.assertTrue(ShiftSlot.objects.filter(name='Custom').exists())

    def test_should_create_new_named_slot_with_saved_slot(self):
        self._set_name_and_save_as(name_val='', save_as_val='new-slot')
        constraint_creator = SlotConstraintCreator(self.dummy_slot_data)
        creator = SlotCreator(business=self.manager_business, slot_data=self.dummy_slot_data,
                              constraint_creator=constraint_creator)

        creator.create()

        self.assertTrue(SavedSlot.objects.filter(name='new-slot').exists())
        self.assertTrue(ShiftSlot.objects.filter(name='new-slot').exists())

    def test_should_raise_DoesNotExist_when_non_existing_saved_slot(self):
        self._set_name_and_save_as(name_val='existing-slot', save_as_val='')
        constraint_creator = SlotConstraintCreator(self.dummy_slot_data)
        creator = SlotCreator(business=self.manager_business, slot_data=self.dummy_slot_data,
                              constraint_creator=constraint_creator)
        self.assertRaises(ObjectDoesNotExist, creator.create)

    def test_should_create_from_existing_save_slot(self):
        existing_name = 'existing-slot'
        SavedSlot.objects.create(name=existing_name, constraints='')
        self._set_name_and_save_as(name_val=existing_name, save_as_val='')
        constraint_creator = SlotConstraintCreator(self.dummy_slot_data)
        creator = SlotCreator(business=self.manager_business, slot_data=self.dummy_slot_data,
                              constraint_creator=constraint_creator)
        creator.create()

        self.assertTrue(ShiftSlot.objects.filter(name=existing_name).exists())

    def _set_name_and_save_as(self, name_val, save_as_val):
        self.dummy_slot_data['name'] = name_val
        self.dummy_slot_data['save_as'] = save_as_val
