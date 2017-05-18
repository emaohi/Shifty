from django.contrib.auth.models import User, Group
from django.test import TestCase, override_settings


class SimpleTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
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
            data['employee_%s_email' % i] = 'yoyo@yoyo.com'
            data['employee_%s_role' % i] = 'WA'
        data['dummy'] = 'dummy'

        return data

    @override_settings(DEBUG=True)
    def test_check_new_employee_group(self):

        self.client.post('/add_employees/', self.make_data(1), follow=True)

        num_results = User.objects.filter(username='RoniL').count()

        self.assertGreater(num_results, 0)

    def test_check_same_username_appends(self):
        data = {'employee_0_firstName': 'Roni', 'employee_0_lastName': 'Levi',
                'employee_0_email': 'emaohi@gmail.com', 'employee_0_role': 'WA',
                'employee_1_firstName': 'Roni', 'employee_1_lastName': 'Lewis',
                'employee_1_email': 'emaohi@gmail.com', 'employee_1_role': 'WA', 'yossi': 'moti'}

        self.client.post('/add_employees/', self.make_data(2), follow=True)

        num_results = User.objects.filter(username__contains='RoniL').count()

        print User.objects.filter(username__contains='RoniL')

        self.assertGreater(num_results, 1)

    def test_should_not_permit_for_regular_employee(self):

        self.client.post('/logout/', follow=True)

        new_credentials = {'username': 'regular', 'password': '123'}

        new_user = User.objects.create_user(**new_credentials)
        Group.objects.get(name='Employees').user_set.add(new_user)

        self.client.post('/login/', new_credentials, follow=True)

        self.client.post('/add_employees/', self.make_data(1), follow=True)

        self.assertEqual(User.objects.filter(username__contains='RoniL').count(), 0)
