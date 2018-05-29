import logging
import random
import string
from time import time
from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand

from log.models import EmployeeProfile, Business

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'populate DB with emp_num employees. roles and business are picked randomly...'

    def add_arguments(self, parser):
        parser.add_argument('emp_num', type=int)

    def _create_employees(self, num):
        for i in range(num):
            created_user = User.objects.create_user(username=self._create_username(i), password=self._create_password(),
                                                    email=self._create_email())
            self.set_emp(created_user)

    def set_emp(self, created_user):
        role = self._pick_role()
        business = self._pick_business()

        logger.info('creating employee username: %s, role: %s in business: %s', created_user.username, role, business)

        emp = created_user.profile
        emp.business = business
        emp.role = role
        emp.save()
        Group.objects.get(name='Employees').user_set.add(created_user)

    def handle(self, *args, **options):
        start_time = time()
        self._create_employees(options['emp_num'])
        end_time = time()
        logger.info('population took: %s seconds', end_time - start_time)

    @staticmethod
    def _create_username(i):
        return 'user' + str(i) + '_' + str(time())

    @staticmethod
    def _create_password():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    def _create_email(self):
        domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com"]
        letters = string.ascii_lowercase[:12]
        return self.get_random_name(letters, 6) + '@' + random.choice(domains)

    @staticmethod
    def get_random_name(letters, length):
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def _pick_role():
        return random.choice([choice[0] for choice in EmployeeProfile.ROLE_CHOICES if choice[1] != 'Manager'])

    @staticmethod
    def _pick_business():
        return random.choice(Business.objects.all())
