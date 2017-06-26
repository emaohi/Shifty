from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


@shared_task
def send_mail(recipient, subject, text, html_to_render, context):

    template_to_render = get_template(html_to_render)
    html_content = template_to_render.render(context)
    message = EmailMultiAlternatives(subject,
                                     text,
                                     'shifty.moti@gmail.com', [recipient])
    message.attach_alternative(html_content, 'text/html')
    message.send()

