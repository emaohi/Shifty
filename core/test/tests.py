from django.contrib.auth.models import User, Group
from django.test import TestCase

from core.models import ManagerMessage
from core.test.test_utils import set_employee, create_new_manager
from log.test.test_utils import make_data


class ManagerMessageTest(TestCase):
    def setUp(self):

        credentials = create_new_manager()
        Group.objects.create(name='Employees')

        self.client.post('/login/', credentials, follow=True)

    def test_status_changed_appears_right_for_employee(self):
        pass

    def test_broadcast_msg_should_appear_for_every_employee(self):

        num_emps = 5
        try:
            self.client.post('/manager/add_employees/', make_data(num_emps), follow=True)

            self.client.post('/core/broadcast_message/', {'subject': 'subject', 'text': 'text'}, follow=True)
        except Exception as e:
            print str(e)

        msg = ManagerMessage.objects.first()
        num_recipients = len(msg.recipients.all())
        num_business_employees = len(msg.business.get_employees())

        print 'num of recipients is %s and num of business employees is %s' %\
              (str(num_recipients), str(num_business_employees))

        self.assertEqual(num_recipients, num_business_employees)
        self.assertEqual(num_recipients, num_emps+1)


class EmployeeRequestTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser1',
            'password': 'secret'
        }
        new_user = User.objects.create_user(**self.credentials)

        Group.objects.create(name='Managers')
        Group.objects.create(name='Employees')

        set_employee(new_user)

        self.client.post('/login/', self.credentials, follow=True)

    def test_request_should_appear_for_business_manager(self):
        try:
            self.client.post('/manager/broadcast_msg/', 'broadcast_test', follow=True)
        except Exception as e:
            print str(e)

        num_results = User.objects.filter(username='RoniL').count()

        print User.objects.filter(username__contains='RoniL')

        self.assertGreater(num_results, 0)


class ShiftSlotTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser1',
            'password': 'secret'
        }
        new_user = User.objects.create_user(**self.credentials)

        Group.objects.create(name='Managers')
        Group.objects.create(name='Employees')

        Group.objects.get(name='Managers').user_set.add(new_user)

        self.client.post('/login/', self.credentials, follow=True)

    def test_add_shift_slot(self):
        pass
