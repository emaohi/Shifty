import logging
from abc import ABCMeta, abstractmethod
from django.db import transaction

from core.models import Shift

logger = logging.getLogger('cool')


class AbstractShiftGenerator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate(self):
        pass


class NaiveShiftGenerator(AbstractShiftGenerator):

    def __init__(self, slots):
        self.slots = slots

    def generate(self):
        with transaction.atomic():
            for slot in self.slots:
                logger.info('Going to make shifts for slots: %s', str(self.slots))
                employees = self._naively_find_employees_for_shift(shift_slot=slot)
                shift = Shift.objects.create(slot=slot)
                shift.employees.add(*[employee.id for employee in employees])

    def _naively_find_employees_for_shift(self, shift_slot):
        all_emps = []
        for role in shift_slot.get_constraints_json():
            all_emps += self._fetch_number_of_role_employees(shift_slot.business, role,
                                                             shift_slot.get_constraint_num_of_role(role))
        return all_emps

    @staticmethod
    def _fetch_number_of_role_employees(business, role, num_of_role_emps):
        business_role_emps = business.get_role_employees(role)
        return business_role_emps[:num_of_role_emps]
