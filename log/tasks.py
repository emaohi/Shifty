from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


@shared_task
def send_mail(_dict):
    to_email = _dict['to_email']
    del _dict['to_email']

    htmly = get_template('manager/new_employee_email_msg.html')
    html_content = htmly.render(_dict)
    message = EmailMultiAlternatives('Sent from Shifty App',
                                     '%s add you as a %s to the businnes %s in Shifty app.'
                                     ' username: %s, password: %s' % (_dict.get('manager'), _dict.get('role'),
                                                                      _dict.get('business'),
                                                                      _dict.get('username'),
                                                                      _dict.get('password')),
                                     'shifty.moti@gmail.com', [to_email])
    message.attach_alternative(html_content, 'text/html')
    message.send()
