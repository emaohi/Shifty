import logging
from time import sleep

from abc import ABCMeta, abstractmethod
from django.db import transaction

from core.models import Shift
from log.models import EmployeeProfile

logger = logging.getLogger(__name__)


class AbstractShiftGenerator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, slots):
        self.slots = list(slots)
        logger.info('Going to deliberately wait....')
        self.wait()

    @abstractmethod
    def wait(self):
        pass

    @abstractmethod
    def add_employees_to_shifts(self):
        pass

    def generate(self):
        logger.info('Going to make shifts for slots: %s, using %s generator', str(self.slots), type(self))
        try:
            with transaction.atomic():
                self.validate_slots()
                self.create_new_shifts()
                self.add_employees_to_shifts()
        except ValueError as e:
            logger.debug('rolling back shift generation transaction: %s', e)
            raise e

    def get_business(self):
        return self.slots[0].business

    def create_new_shifts(self):
        for slot in self.slots:
            slot.delete_existing_shift()
            Shift.objects.create(slot=slot)

    def _get_total_required_map(self):
        total_dict = {}
        for role in EmployeeProfile.get_employee_roles():
            total_dict[role] = self._get_total_required_of_role(role.lower())
        return total_dict

    def _get_total_required_of_role(self, role):
        total_role = 0
        for slot in self.slots:
            total_role += slot.get_constraint_num_of_role(role)
        return total_role

    def validate_slots(self):
        for role in EmployeeProfile.get_employee_roles():
            self.validate_role(role)

    def validate_role(self, role):
        slot_with_max_emps = max(self.slots, key=lambda slot: slot.get_constraint_num_of_role(role.lower()))
        num_of_role_in_business = len(self.get_business().get_role_employees(role))
        max_slot_num = slot_with_max_emps.get_constraint_num_of_role(role.lower())
        if num_of_role_in_business < max_slot_num:
            logger.error('number of %s in business %s is less the required for the max slot (%s < %s)',
                         role, self.get_business(), num_of_role_in_business, max_slot_num)
            raise ValueError('too few %ss' % role)


class NaiveShiftGenerator(AbstractShiftGenerator):

    def __init__(self, slots):
        super(NaiveShiftGenerator, self).__init__(slots)

    def wait(self):
        sleep(1)

    def add_employees_to_shifts(self):
        for slot in self.slots:
            employees = self._find_employees_for_slot(slot)
            slot.shift.employees.add(*[emp.id for emp in employees])

    def _find_employees_for_slot(self, slot):
        all_emps = []
        for role in slot.get_constraints_json():
            all_emps += self._fetch_number_of_role_employees(slot.business, role,
                                                             slot.get_constraint_num_of_role(role))
        return all_emps

    @staticmethod
    def _fetch_number_of_role_employees(business, role, num_of_role_emps):
        business_role_emps = business.get_role_employees(role)
        return business_role_emps[:num_of_role_emps]


class ThoughtfulShiftGenerator(AbstractShiftGenerator):

    def __init__(self, slots):
        super(ThoughtfulShiftGenerator, self).__init__(slots)

    def add_employees_to_shifts(self):
        emps_per_role = [self.get_business().get_waiters(), self.get_business().get_bartenders(),
                         self.get_business().get_cooks()]
        total_role_required_map = self._get_total_required_map()
        for role_emps in emps_per_role:
            logger.debug('Going to add %r to shifts', role_emps)
            self._add_role_emps_to_shifts(role_emps, role_emps[0].get_role_display(), total_role_required_map)

    def wait(self):
        sleep(1)

    def _add_role_emps_to_shifts(self, role_emps, role, totals_map):
        slots_iterator = iter(self.slots)
        curr_slot = next(slots_iterator)
        while totals_map[role] > 0:
            not_chosen_ordered = self._get_sorted_by_slot(role_emps, curr_slot)

            while len(not_chosen_ordered) > 0:
                if len(not_chosen_ordered) < curr_slot.get_constraint_num_of_role(role.lower()):
                    break

                self._put_not_chosen(curr_slot, not_chosen_ordered, role, totals_map)

                try:
                    curr_slot = next(slots_iterator)
                except StopIteration:
                    break

    @staticmethod
    def _put_not_chosen(next_slot, not_chosen_ordered, role, totals_map):
        for _ in range(next_slot.get_constraint_num_of_role(role.lower())):
            emp = not_chosen_ordered.pop(0)
            next_slot.shift.employees.add(emp)
            totals_map[role] -= 1

    @staticmethod
    def _get_sorted_by_slot(emps, slot):
        return sorted(emps, key=slot.is_emp_requested)


class ShiftGeneratorFactory:

    def __init__(self):
        pass

    @staticmethod
    def create(level, slots):
        if level == 0:
            return NaiveShiftGenerator(slots)
        if level == 1:
            return ThoughtfulShiftGenerator(slots)
