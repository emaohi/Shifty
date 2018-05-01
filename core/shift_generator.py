import logging
from time import sleep

from abc import ABCMeta, abstractmethod
from django.db import transaction

from core.models import Shift

logger = logging.getLogger(__name__)


class AbstractShiftGenerator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        logger.info('Going to deliberately wait....')
        self.wait()

    @abstractmethod
    def wait(self):
        pass

    def generate(self, slots):
        logger.info('Going to make shifts for slots: %s, using %s generator', str(slots), type(self))
        try:
            with transaction.atomic():
                self.generate_shifts_from_slots(slots)
        except (ValueError, TypeError) as e:
            logger.debug('rolling back shift generation transaction: %s', e)
            raise e

    @abstractmethod
    def generate_shifts_from_slots(self, slots):
        pass


class NaiveShiftGenerator(AbstractShiftGenerator):

    def __init__(self):
        super(NaiveShiftGenerator, self).__init__()

    def wait(self):
        sleep(7)

    def generate_shifts_from_slots(self, slots):
        for slot in slots:
            slot.delete_existing_shift()
            shift = Shift.objects.create(slot=slot)
            employees = self._find_employees_for_slot(slot)
            shift.employees.add(*[emp.id for emp in employees])

    def _find_employees_for_slot(self, slot):
        all_emps = []
        for role in slot.get_constraints_json():
            all_emps += self._fetch_number_of_role_employees(slot.business, role,
                                                             slot.get_constraint_num_of_role(role))
        return all_emps

    @staticmethod
    def _fetch_number_of_role_employees(business, role, num_of_role_emps):
        business_role_emps = business.get_role_employees(role)
        if len(business_role_emps) < num_of_role_emps:
            logger.error('number of %s in business %s is less the required for the slot (%s < %s)',
                         role, business, len(business_role_emps), num_of_role_emps)
            raise ValueError('too few %ss' % role)
        return business_role_emps[:num_of_role_emps]


class ThoughtfulShiftGenerator(AbstractShiftGenerator):

    def __init__(self):
        super(ThoughtfulShiftGenerator, self).__init__()

    def generate_shifts_from_slots(self, slots):
        pass

    def wait(self):
        sleep(10)


class ShiftGeneratorFactory:

    def __init__(self):
        pass

    @staticmethod
    def create(level):
        if level == 0:
            return NaiveShiftGenerator()
        if level == 1:
            return ThoughtfulShiftGenerator()
