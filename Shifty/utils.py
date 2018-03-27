import logging
from django.conf import settings
from time import time

from django.http import HttpResponseBadRequest

from Shifty import tasks

logger = logging.getLogger(__name__)


def send_multiple_mails_with_html(subject, text, template, r_2_c_dict, wait_for_results=True):

    is_celery = settings.CELERY
    async_tasks = []

    logger.info('recp list is: %s', str(r_2_c_dict))

    recp_list = {recip: value for recip, value in r_2_c_dict.iteritems() if recip.profile.enable_mailing}

    for recp, context in recp_list.iteritems():
        send_mail_params = [recp.email, subject, text, template, context]
        async_tasks.append(tasks.send_mail.delay(*send_mail_params) if is_celery else
                           tasks.send_mail(*send_mail_params))

    if is_celery and wait_for_results:
        if not wait_for_tasks_to_be_completed(async_tasks):
            raise EmailWaitError('Waited too much for mails to be sent')


def now_millis():
    return int(round(time() * 1000))


def wait_for_tasks_to_be_completed(celery_tasks):
    timeout_millis = settings.CELERY_MAIL_TIMEOUT
    time_to_stop = now_millis() + timeout_millis
    while time_to_stop > now_millis():
        if all([result.status == 'SUCCESS' for result in celery_tasks]):
            return True
    logger.warn('not all celery tasks finished/succeeded before timeout')
    return False


class EmailWaitError(Exception):
    def __init__(self, message):
        super(EmailWaitError, self).__init__(message)
        self.message = 'SERVER ERROR - EMAIL ERROR - %s' % self.message


def must_be_manager_callback(user):
    if user.groups.filter(name='Managers').exists():
        return True
    logger.error('cant proceed - not manager')
    return False


def must_be_employee_callback(user):
    if user.groups.filter(name='Employees').exists():
        return True
    logger.error('cant proceed - you are a manager !')
    return False


def get_curr_profile(request):
    return request.user.profile


def get_curr_business(request):
    return get_curr_profile(request).business


def wrong_method(request):
    return HttpResponseBadRequest('cannot get here with ' + request.method)


def get_logo_conf():
    return dict(format="png", transformation=[
        dict(crop="fit", width=80, height=50, radius=10),
        dict(angle=20)
    ]) if settings.DEFAULT_FILE_STORAGE.startswith('cloud') else ''

