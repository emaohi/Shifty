from django.utils import timezone
from django.http import HttpResponse

from core.models import Message, EmployeeRequest


def report_incorrect_detail(request):
    if request.method == 'POST':
        reporting_profile = request.user.profile
        incorrect_field = request.POST.get('incorrect_field')
        fix_suggestion = request.POST.get('fix_suggestion')
        curr_val = request.POST.get('curr_val')

        new_request = EmployeeRequest(sent_time=timezone.now(),
                                      subject='Employee Data Change Request',
                                      text='%s have mentioned that his %s field is incorrect.'
                                           ' Current field value is %s; His suggestion is %s' %
                                      (reporting_profile.user.username, incorrect_field, curr_val, fix_suggestion))
        new_request.save()
        # add the employee's manager to the recipients list
        new_request.issuers.add(reporting_profile)

        return HttpResponse('Report was sent successfully')
