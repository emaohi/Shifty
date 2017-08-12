from django.contrib.auth.models import Group, User


def set_manager(new_user):
    Group.objects.get(name='Managers').user_set.add(new_user)
    new_user.profile.business.manager = new_user
    new_user.profile.business.save()


def set_employee(new_user):
    Group.objects.get(name='Employees').user_set.add(new_user)


def create_new_manager():
    credentials = {
        'username': 'testuser1',
        'password': 'secret'
    }
    new_user = User.objects.create_user(**credentials)

    Group.objects.create(name='Managers')

    set_manager(new_user)

    return credentials
