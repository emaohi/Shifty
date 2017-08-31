from django.contrib.auth.models import Group, User


def create_manager_and_employee_groups():
    Group.objects.create(name='Employees')
    Group.objects.create(name='Managers')


def set_manager(new_user):
    Group.objects.get(name='Managers').user_set.add(new_user)
    new_user.profile.role = 'MA'
    new_user.profile.save()
    new_user.profile.business.manager = new_user
    new_user.profile.business.save()


def set_employee(new_user):
    Group.objects.get(name='Employees').user_set.add(new_user)
    new_user.profile.role = 'WA'
    new_user.profile.save()


def create_new_manager(cred_dict):
    new_user = User.objects.create_user(**cred_dict)
    set_manager(new_user)
    disable_mailing(new_user)


def create_new_employee(cred_dict):
    new_user = User.objects.create_user(**cred_dict)
    set_employee(new_user)
    disable_mailing(new_user)


def disable_mailing(user):
    user.profile.enable_mailing = False
    user.profile.save()
