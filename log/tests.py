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

    @override_settings(DEBUG=True)
    def test_check_new_employee_group(self):

        data = {'employee_0_firstName': 'Roni', 'employee_0_lastName': 'Levi',
                'employee_0_email': 'emaohi@gmail.com', 'employee_0_role': 'WA', 'yossi': 'moti'}

        response = self.client.post('/login/', self.credentials, follow=True)

        print 'login response is', str(response.status_code)

        response = self.client.post('/add_employees/', data, follow=True)

        print 'add_employee response is', str(response.status_code)

        should_be_username = 'RoniL'

        num_results = User.objects.filter(username=should_be_username).count()

        print response.content

        self.assertGreater(num_results, 0)
