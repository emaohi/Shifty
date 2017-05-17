import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail


class NewEmployeeHandler:
    def __init__(self, first_name, last_name, email, role, manager_user):
        self.firs_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.manager = manager_user
        self.user_created = None
        self.password_created = None

    def create_employee(self):
        username = self._generate_username()
        self.password_created = self._generate_password(6)

        self.user_created = User.objects.create_user(username=username, password=self.password_created,
                                                     email=self.email,
                                                     first_name=self.firs_name, last_name=self.last_name)

        new_profile = self.user_created.profile
        new_profile.business = self.manager.profile.business
        new_profile.role = self.role
        new_profile.save()

        return self.user_created

    def send_invitation_mail(self):
        send_mail(
            'Sent from Shifty App',
            '%s add you as a %s to the businnes %s in Shifty app. username: %s, password: %s' %
            (self.manager.username, self.role, self.manager.profile.business.business_name,
             self.user_created.username, self.password_created),
            'shifty.moti@gmail.com',
            [self.user_created.email],
            fail_silently=False,
        )

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
