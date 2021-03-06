import random
import string

import logging


from django.contrib.auth.models import User

from Shifty.utils import send_multiple_mails_with_html

logger = logging.getLogger(__name__)


class NewEmployeeHandler:
    def __init__(self, first_name, last_name, email, role, date_joined, manager_user):
        self.firs_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.date_joined = date_joined
        self.manager = manager_user
        self.user_created = None
        self.password_created = None

    def create_employee(self):

        username = self._generate_username()
        self.password_created = generate_password(6)

        self.user_created = User.objects.create_user(username=username, password=self.password_created,
                                                     email=self.email,
                                                     first_name=self.firs_name, last_name=self.last_name)

        new_profile = self.user_created.profile
        new_profile.business = self.manager.profile.business
        new_profile.role = self.role
        new_profile.started_work_date = self.date_joined
        new_profile.save()

        return self.user_created

    def get_invitation_mail_details(self):
        return {'manager': self.manager.username, 'role': self.user_created.profile.get_role_display(),
                'business': self.manager.profile.business.business_name, 'username': self.user_created.username,
                'password': self.password_created, 'first_name': self.firs_name, 'to_email': self.user_created}

    def _generate_username(self):
        # first name and last letter of last name
        suggested_username = self.firs_name + self.last_name[0]

        existing_users = User.objects.filter(username__contains=suggested_username).order_by('date_joined')

        # this username doesnt exist - return it
        if existing_users.count() == 0:
            return suggested_username

        last_added = existing_users.last()
        split_name = last_added.username.split('_')

        if len(split_name) == 1:
            return last_added.username + '_1'
        else:
            curr = int(split_name[1])
            return '%s_%s' % (split_name[0], str(curr+1))


def send_new_employees_mails(mail_dicts=None):

    recipients = [_dict['to_email'] for _dict in mail_dicts]
    # remove non-serializable form dicts
    for _dict in mail_dicts:
        _dict.pop('to_email')

    recipient_to_context_dict = dict(zip(recipients, mail_dicts))

    send_multiple_mails_with_html(subject='Sent from Shifty App',
                                  text='you\'ve been added to shifty as an employee',
                                  template='html_msgs/new_employee_email_msg.html',
                                  r_2_c_dict=recipient_to_context_dict, wait_for_results=False, update_emp=True)


def generate_password(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))