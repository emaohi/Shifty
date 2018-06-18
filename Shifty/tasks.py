from __future__ import absolute_import, unicode_literals

import logging
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

logger = logging.getLogger(__name__)


@shared_task
def send_mail(recipient, subject, text, html_to_render, context, recipient_id=None):

    template_to_render = get_template(html_to_render)
    html_content = template_to_render.render(context)
    message = EmailMultiAlternatives(subject,
                                     text,
                                     'shifty.moti@gmail.com', [recipient])
    message.attach_alternative(html_content, 'text/html')
    message.send()

    if recipient_id:
        logger.info('going to set true credentials_sent of emp id %s', recipient_id)
        recp = User.objects.get(pk=recipient_id)
        recp.profile.credentials_sent = True
        recp.save()
