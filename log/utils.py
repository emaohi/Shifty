import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class NewEmployeeHandler:
    def __init__(self, first_name, last_name, email):
        self.firs_name = first_name
        self.last_name = last_name
        self.email = email
        self.user = None

    def create_employee(self):
        username = self._generate_username()
        password = self._generate_password(6)

        self.user = User.objects.create_user(username=username, password=password, email=self.email)

    def send_invitation_mail(self):
        pass

    def _generate_username(self):
        suggested_username = self.firs_name + self.last_name[-1]
        try:
            existing_user = User.objects.get(username__contains=suggested_username)
        except ObjectDoesNotExist:
            return suggested_username

        split_name = existing_user.user_name.split('_')
        if len(split_name) == 0:
            return existing_user.username + '_1'
        else:
            curr = int(split_name[1])
            return '%s_%s' % (split_name[0], str(curr+1))

    @staticmethod
    def _generate_password(length):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
