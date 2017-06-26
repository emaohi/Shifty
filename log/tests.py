import datetime
from django.contrib.auth.models import User, Group
from django.test import TestCase, override_settings


class AddEmployeesTest(TestCase):
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

    @staticmethod
    def make_data(n):
        data = {}
        for i in range(n):
            data['employee_%s_firstName' % i] = 'Roni'
            data['employee_%s_lastName' % i] = 'L' + str(i)
            data['employee_%s_email' % i] = 'emaohi@gmail.com'
            data['employee_%s_role' % i] = 'WA'
            data['employee_%s_dateJoined' % i] = datetime.date.today()
        data['dummy'] = 'dummy'

        return data

    @override_settings(DEBUG=True)
    def test_check_new_employee_group(self):

        try:
            self.client.post('/manager/add_employees/', self.make_data(1), follow=True)
        except Exception as e:
            print str(e)

        num_results = User.objects.filter(username='RoniL').count()

        print User.objects.filter(username__contains='RoniL')

        self.assertGreater(num_results, 0)

    def test_check_same_username_appends(self):

        self.client.post('/manager/add_employees/', self.make_data(2), follow=True)

        num_results = User.objects.filter(username__contains='RoniL').count()

        print User.objects.filter(username__contains='RoniL')

        self.assertGreater(num_results, 1)

    def test_should_not_permit_for_regular_employee(self):

        self.client.post('/logout/', follow=True)

        new_credentials = {'username': 'regular', 'password': '123'}

        new_user = User.objects.create_user(**new_credentials)
        Group.objects.get(name='Employees').user_set.add(new_user)

        self.client.post('/login/', new_credentials, follow=True)

        self.client.post('/manager/add_employees/', self.make_data(1), follow=True)

        self.assertEqual(User.objects.filter(username__contains='RoniL').count(), 0)
