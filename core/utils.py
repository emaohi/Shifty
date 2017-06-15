from django.utils import timezone

from core.models import ManagerMessage


def send_manager_msg(emp_request):
    recipients = emp_request.issuers.all()
    curr_business = recipients.first().business
    new_status = emp_request.get_status_display()

    manager_msg = ManagerMessage(business=curr_business, sent_time=timezone.now(),
                                 subject='Request status changed',
                                 text='Your following request has been %s by your manager:\n%s' %
                                      (new_status, emp_request.text))
    manager_msg.save()

    manager_msg.recipients = recipients
    manager_msg.save()
