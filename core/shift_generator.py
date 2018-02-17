import logging
from abc import ABCMeta, abstractmethod
from django.db import transaction

from core.models import Shift

logger = logging.getLogger('cool')


class AbstractShiftGenerator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate(self):
        pass


class NaiveShiftGenerator(AbstractShiftGenerator):

    def __init__(self, slots):
        super(NaiveShiftGenerator, self).__init__()
        self.slots = slots

    def generate(self):
        logger.info('Going to make shifts for slots: %s', str(self.slots))
        with transaction.atomic():
            for slot in self.slots:
                existing_slots = Shift.objects.filter(slot=slot)
                logger.info('Going to delete %d shifts for slot %s', existing_slots.count(), str(slot))
                existing_slots.delete()

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
