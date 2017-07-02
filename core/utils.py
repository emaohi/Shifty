import itertools
from django.utils import timezone

from core.models import ManagerMessage, EmployeeRequest
from log.utils import send_multiple_mails_with_html


def create_manager_msg(recipients, subject, text):
    curr_business = recipients.first().business
    manager_msg = ManagerMessage(business=curr_business, sent_time=timezone.now(),
                                 subject=subject, text=text)
    manager_msg.save()

    manager_msg.recipients = recipients
    manager_msg.save()

    # # send emails
    recipient_users = [r.user for r in recipients]
    recipient_to_context_dict = dict(zip(recipient_users,
                                         itertools.repeat({'manager': curr_business.manager.username})))
    template = 'html_msgs/new_manager_message_email_msg.html'
    subject = 'New message in Shifty app'
    text = 'you\'ve got new message from your manger'

    send_multiple_mails_with_html(subject=subject, text=text,
                                  template=template, r_2_c_dict=recipient_to_context_dict)


def get_manger_msgs_of_employee(employee):
    return ManagerMessage.objects.filter(recipients__in=[employee]).order_by('-sent_time')


def get_employee_requests_with_status(manager, status):
    business_employees = manager.business.get_employees()
    return EmployeeRequest.objects.filter(issuers__in=business_employees, status=status). \
        distinct()


def send_mail_to_manager(emp_user):
    send_multiple_mails_with_html(subject='New message in Shifty app',
                                  text='you\'ve got new message from %s' % emp_user.username,
                                  template='html_msgs/new_employee_change_request.html',
                                  r_2_c_dict={emp_user.profile.business.manager:
                                                  {'employee_first_name': emp_user.first_name,
                                                   'employee_last_name': emp_user.last_name}})
