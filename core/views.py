from django.utils import timezone
from django.http import HttpResponse

from core.models import Message


def report_incorrect_detail(request):
    if request.method == 'POST':
        reporting_profile = request.user.profile
        incorrect_field = request.POST.get('incorrect_field')
        fix_suggestion = request.POST.get('fix_suggestion')

        new_msg = Message(sender=reporting_profile, sent_time=timezone.now(), subject='Incorrect Employee Data',
                          text='%s have mentioned that his %s is incorrect; his suggestion is %s' %
                               (reporting_profile.user.username, incorrect_field, fix_suggestion))
        new_msg.save()
        new_msg.recipients.add(reporting_profile.get_manager())

        return HttpResponse('Report was sent successfully')
