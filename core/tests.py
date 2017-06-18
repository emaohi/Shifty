from django.contrib.auth.models import User, Group
from django.test import TestCase, override_settings


class ManagerMessageTest(TestCase):
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

    def test_msg_should_appear_for_every_employee(self):
        try:
            self.client.post('/manager/broadcast_msg/', 'broadcast_test', follow=True)
        except Exception as e:
            print str(e)

        num_results = User.objects.filter(username='RoniL').count()

        print User.objects.filter(username__contains='RoniL')

        self.assertGreater(num_results, 0)


class BroadcastMessageTest(TestCase):
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

    def test_msg_should_appear_for_every_employee(self):
        try:
            self.client.post('/manager/broadcast_msg/', 'broadcast_test', follow=True)
        except Exception as e:
            print str(e)

        num_results = User.objects.filter(username='RoniL').count()

        print User.objects.filter(username__contains='RoniL')

        self.assertGreater(num_results, 0)
