from django.utils import timezone

from core.models import ManagerMessage, EmployeeRequest


def create_manager_msg(recipients, subject, text):
    curr_business = recipients.first().business
    manager_msg = ManagerMessage(business=curr_business, sent_time=timezone.now(),
                                 subject=subject, text=text)
    manager_msg.save()

    manager_msg.recipients = recipients
    manager_msg.save()


def get_manger_msgs_of_employee(employee):
    return ManagerMessage.objects.filter(recipients__in=[employee]).order_by('-sent_time')


def get_employee_requests_with_status(manager, status):
    business_employees = manager.business.get_employees()
    return EmployeeRequest.objects.filter(issuers__in=business_employees, status=status). \
        distinct()
