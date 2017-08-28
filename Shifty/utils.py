import logging
from django.conf import settings
from time import time

from Shifty import tasks

logger = logging.getLogger('cool')


def send_multiple_mails_with_html(subject, text, template, r_2_c_dict, wait_for_results=True):
    def now_millis():
        """returns current timestamp in millis"""
        return int(round(time() * 1000))

    is_celery = settings.CELERY
    task_results = []

    recp_list = {recip: value for recip, value in r_2_c_dict.iteritems() if recip.profile.enable_mailing}

    for recp, context in recp_list.iteritems():
        send_mail_params = [recp.email, subject, text, template, context]
        task_results.append(tasks.send_mail.delay(*send_mail_params) if is_celery else
                            tasks.send_mail(*send_mail_params))

    if is_celery and wait_for_results:
        timeout_millis = settings.CELERY_MAIL_TIMEOUT
        time_to_stop = now_millis() + timeout_millis
        while time_to_stop > now_millis():
            if all([result.status == 'SUCCESS' for result in task_results]):
                return True
        raise EmailWaitError('Waited too much for mails to be sent')


class EmailWaitError(Exception):
    def __init__(self, message):
        super(EmailWaitError, self).__init__(message)
        self.message = 'SERVER ERROR - EMAIL ERROR - %s' % self.message


def must_be_manager_callback(user):
    if user.groups.filter(name='Managers').exists():
        return True
    logger.error('cant proceed - not manager')
    return False
