import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class NewEmployeeHandler:
    def __init__(self, first_name, last_name, email, business):
        self.firs_name = first_name
        self.last_name = last_name
        self.email = email
        self.business = business
        self.user = None

    def create_employee(self):
        username = self._generate_username()
        password = self._generate_password(6)

        self.user = User.objects.create_user(username=username, password=password, email=self.email)

        new_profile = self.user.profile
        new_profile.business = self.business
        new_profile.save()

        return self.user.username

    def send_invitation_mail(self):
        pass

    def _generate_username(self):
        # first name and last letter of last name
        suggested_username = self.firs_name + self.last_name[0]

        existing_users = User.objects.filter(username__contains=suggested_username).order_by('date_joined')

        # this username doesnt exist - return it
        if len(existing_users) == 0:
            return suggested_username

        last_added = existing_users[-1]
        split_name = last_added.user_name.split('_')

        if len(split_name) == 1:
            return last_added.username + '_1'
        else:
            curr = int(split_name[1])
            return '%s_%s' % (split_name[0], str(curr+1))

    @staticmethod
    def _generate_password(length):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
