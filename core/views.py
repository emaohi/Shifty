from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse

from core.models import Message


def report_incorrect_detail(request):
    if request.method == 'POST':
        reporting_profile = request.user.profile
        incorrect_field = request.POST.get('incorrect_field')
        fix_suggestion = request.POST.get('fix_suggestion')

        new_msg = Message(sender=reporting_profile, sent_time=timezone.now(), subject='Incorrect Employee Data',
                          text='%s have mentioned that his %s field is incorrect; His suggestion is %s' %
                               (reporting_profile.user.username, incorrect_field, fix_suggestion))
        new_msg.save()
        # add the employee's manager to the recipients list
        new_msg.recipients.add(reporting_profile.get_manager())

        return HttpResponse('Report was sent successfully')


@login_required(login_url="/login")
@user_passes_test(lambda user: user.groups.filter(name='Managers').exists())
def manager_home(request):
    return render(request, "manager/home.html", {'employee_messages': Message.objects.filter(
        recipients__in=[request.user.profile]).order_by('-sent_time')})


@login_required(login_url="/login")
@user_passes_test(lambda user: user.groups.filter(name='Employees').exists(), login_url='/')
def emp_home(request):
    return render(request, "employee/home.html")
