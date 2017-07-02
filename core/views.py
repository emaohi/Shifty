import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError

from core.models import EmployeeRequest
from core.utils import create_manager_msg, send_mail_to_manager

from Shifty.utils import must_be_manager_callback, EmailWaitError
from .forms import *

logger = logging.getLogger('cool')


@login_required(login_url='/login')
def report_incorrect_detail(request):
    if request.method == 'POST':
        reporting_profile = request.user.profile
        incorrect_field = request.POST.get('incorrect_field')
        fix_suggestion = request.POST.get('fix_suggestion')
        curr_val = request.POST.get('curr_val')

        logger.info('creating new employee request')
        new_request = EmployeeRequest(sent_time=timezone.now(),
                                      subject='Employee Change Request',
                                      text='Field claimed to be incorrect: %s.'
                                           ' Current field value is %s; Suggestion is %s' %
                                      (incorrect_field, curr_val, fix_suggestion))
        new_request.save()
        # add the employee's manager to the recipients list
        new_request.issuers.add(reporting_profile)

        send_mail_to_manager(request.user)

        return HttpResponse('Report was sent successfully')


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def handle_employee_request(request):
    if request.method == 'POST':
        emp_request_id = request.POST.get('emp_request_id')
        new_status = request.POST.get('new_status')

        emp_request = EmployeeRequest.objects.get(id=emp_request_id)
        emp_request.status = new_status
        emp_request.save()

        logger.info('creating manager msg in response to the employee request')
        create_manager_msg(recipients=emp_request.issuers.all(), subject='Your request status has been changed',
                           text='Your following request has been %s by your manager:\n %s' %
                           (emp_request.get_status_display(), emp_request.text))

        messages.success(request, message='request approved' if new_status == 'A' else 'request rejected')
        return HttpResponse('ok')


@login_required(login_url='/login')
@user_passes_test(lambda user: user.groups.filter(name='Managers').exists())
def broadcast_message(request):
    if request.method == 'POST':
        broadcast_form = BroadcastMessageForm(request.POST)

        if broadcast_form.is_valid():
            recipients = request.user.profile.business.get_employees()

            new_manager_msg = broadcast_form.save(commit=False)

            try:
                create_manager_msg(recipients=recipients, subject=new_manager_msg.subject, text=new_manager_msg.text)
            except EmailWaitError as e:
                return HttpResponseServerError(e.message)

            messages.success(request, message='Broadcast message created')
            return HttpResponseRedirect('/')
        else:
            logger.error('broadcast form is not valid')
            form = BroadcastMessageForm()
            messages.error(request, message='couldn\'t send broadcast message' % str(form.errors))
            return HttpResponseRedirect('/')
    else:    # method is GET
        form = BroadcastMessageForm()
        return render(request, 'ajax_form.html', {'form': form})

