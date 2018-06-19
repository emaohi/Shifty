import logging

from celery.schedules import crontab
from celery.task import periodic_task

from log.models import EmployeeProfile
from log.utils import send_new_employees_mails

logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute=0, hour=0))
def retry_new_employees_mail():

    employees_to_retry = EmployeeProfile.objects.filter(credentials_sent=False)
    mail_dicts = [emp.generate_mail_context() for emp in employees_to_retry]
    if not len(mail_dicts):
        logger.info('no employees to update with credentials, all clear :)')
        return 'none to update'
    try:
        logger.info('Trying to update %d employees for their credentials', len(employees_to_retry))
        send_new_employees_mails(mail_dicts=mail_dicts)
    except BaseException as e:
        logger.error('Couldn\'t update emps for their credentials: %s', e.message)
        raise e
