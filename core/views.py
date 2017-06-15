import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import HttpResponse

from core.models import EmployeeRequest
from core.utils import send_manager_msg

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

        return HttpResponse('Report was sent successfully')


@login_required(login_url='/login')
@user_passes_test(lambda user: user.groups.filter(name='Managers').exists())
def handle_employee_request(request):
    if request.method == 'POST':
        emp_request_id = request.POST.get('emp_request_id')
        new_status = request.POST.get('new_status')

        emp_request = EmployeeRequest.objects.get(id=emp_request_id)
        emp_request.status = new_status
        emp_request.save()

        logger.info('creating manager msg in response to the employee request')
        send_manager_msg(emp_request)

        messages.success(request, message='request approved' if new_status is 'A' else 'request rejected')
        return HttpResponse('ok')
