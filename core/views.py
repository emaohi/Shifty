import json
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse, \
    HttpResponseBadRequest

from core.date_utils import get_next_week_num, get_date, get_next_week_string, get_curr_year
from core.models import EmployeeRequest, Holiday
from core.utils import create_manager_msg, send_mail_to_manager, create_constraint_json_from_form, get_holiday_or_none

from Shifty.utils import must_be_manager_callback, EmailWaitError
from log.models import Business
from .forms import *

logger = logging.getLogger('cool')


@login_required(login_url='/login')
def report_incorrect_detail(request):
    if request.method == 'POST':
        reporting_profile = request.user.profile
        incorrect_field = request.POST.get('incorrect_field')
        fix_suggestion = request.POST.get('fix_suggestion')
        curr_val = request.POST.get('curr_val')

        logger.info('creating new employee request')
        new_request = EmployeeRequest(sent_time=timezone.now(),
                                      type='P',
                                      subject='Employee Change Request',
                                      text='Field claimed to be incorrect: %s.'
                                           ' Current field value is %s; Suggestion is %s' %
                                      (incorrect_field, curr_val, fix_suggestion))
        new_request.save()
        # add the employee's manager to the recipients list
        new_request.issuers.add(reporting_profile)
        try:
            send_mail_to_manager(request.user)
        except EmailWaitError as e:
            return HttpResponseServerError(e.message)

        return HttpResponse('Report was sent successfully')


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def handle_employee_request(request):
    if request.method == 'POST':
        emp_request_id = request.POST.get('emp_request_id')
        new_status = request.POST.get('new_status')

        emp_request = EmployeeRequest.objects.get(id=emp_request_id)
        emp_request.status = new_status
        emp_request.save()

        logger.info('creating manager msg in response to the employee request')
        try:
            create_manager_msg(recipients=emp_request.issuers.all(), subject='Your request status has been changed',
                               text='Your following request has been %s by your manager:\n %s' %
                               (emp_request.get_status_display(), emp_request.text))
        except EmailWaitError as e:
            return HttpResponseServerError(e.message)

        messages.success(request, message='request approved' if new_status == 'A' else 'request rejected')
        return HttpResponse('ok')


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def broadcast_message(request):
    if request.method == 'POST':
        broadcast_form = BroadcastMessageForm(request.POST)

        if broadcast_form.is_valid():
            recipients = request.user.profile.business.get_employees()

            new_manager_msg = broadcast_form.save(commit=False)

            try:
                create_manager_msg(recipients=recipients, subject=new_manager_msg.subject, text=new_manager_msg.text)
            except EmailWaitError as e:
                return HttpResponseServerError(e.message)

            messages.success(request, message='Broadcast message created')
            return HttpResponseRedirect('/')
        else:
            logger.error('broadcast form is not valid')
            form = BroadcastMessageForm()
            messages.error(request, message='couldn\'t send broadcast message' % str(form.errors))
            return HttpResponseRedirect('/')
    else:    # method is GET
        form = BroadcastMessageForm()
        return render(request, 'ajax_form.html', {'form': form})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def add_shift_slot(request):
    if request.method == 'POST':
        slot_form = ShiftSlotForm(request.POST)
        if slot_form.is_valid():
            data = slot_form.cleaned_data
            slot_constraint_json = create_constraint_json_from_form(data)

            slot_holiday = get_holiday_or_none(get_curr_year(), data['day'], get_next_week_num())

            holiday = slot_holiday if slot_holiday else None

            new_slot = ShiftSlot(business=request.user.profile.business, day=data['day'],
                                 start_hour=data['start_hour'], end_hour=data['end_hour'],
                                 constraints=json.dumps(slot_constraint_json),
                                 week=get_next_week_num(), holiday=holiday)
            new_slot.save()
            messages.success(request, 'slot form was ok')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'manager/new_shift.html', {'form': slot_form})
    else:
        day = request.GET.get('day', '')
        start_hour = request.GET.get('startTime', '')

        slot_holiday = get_holiday_or_none(get_curr_year(), day, get_next_week_num())

        form = ShiftSlotForm(initial={'day': day, 'start_hour': start_hour.replace('-', ':')})
        return render(request, 'manager/new_shift.html', {'form': form, 'week_range': get_next_week_string(),
                                                          'holiday': slot_holiday})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def update_shift_slot(request, slot_id):

    updated_slot = get_object_or_404(ShiftSlot, id=slot_id)

    if not updated_slot.is_next_week():
        return HttpResponseBadRequest('<h3>this shift is not at next week</h3>')

    if request.method == 'POST':
        logger.info('in post, is is %s' % slot_id)
        slot_form = ShiftSlotForm(request.POST)
        if slot_form.is_valid():
            data = slot_form.cleaned_data
            slot_constraint_json = create_constraint_json_from_form(data)

            logger.info('new end hour is %s' % str(data['end_hour']))
            ShiftSlot.objects.filter(id=slot_id).update(business=request.user.profile.business, day=data['day'],
                                                        start_hour=data['start_hour'], end_hour=data['end_hour'],
                                                        constraints=json.dumps(slot_constraint_json),
                                                        week=get_next_week_num())
            messages.success(request, 'slot updated')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'manager/new_shift.html', {'form': slot_form})
    else:
        logger.info('in get, is is %s' % slot_id)
        day = int(updated_slot.day)
        start_hour = str(updated_slot.start_hour)
        end_hour = str(updated_slot.end_hour)
        form = ShiftSlotForm(initial={'day': day, 'start_hour': start_hour.replace('-', ':'),
                                      'end_hour': end_hour.replace('-', ':')})
        return render(request, 'manager/update_shift.html', {'form': form, 'week_range': get_next_week_string(),
                                                             'id': slot_id, 'holiday': updated_slot.holiday})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def delete_slot(request):

    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        updated_slot = get_object_or_404(ShiftSlot, id=slot_id)
        if not updated_slot.is_next_week():
            return HttpResponseBadRequest('<h3>this shift is not at next week</h3>')

        updated_slot.delete()
        logger.info('shift slow id %s was deleted' % slot_id)
        messages.success(request, 'slot was deleted successfully')
        return HttpResponse('ok')

    return HttpResponseBadRequest('cannot delete with GET')


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def get_next_week_slots(request):
    shifts_json = []

    slot_id_to_constraints_dict = {}

    next_week_no = get_next_week_num()
    next_week_slots = ShiftSlot.objects.filter(week=next_week_no)
    for slot in next_week_slots:
        jsoned_shifts = json.dumps({'id': str(slot.id), 'title': 'Shift Slot %s' % str(slot.id),
                                    'start': slot.start_time_str(),
                                    'end': slot.end_time_str(),
                                    'backgroundColor': '#205067',
                                    'textColor': '#f5dd5d' if not slot.holiday else '#ff7100'})
        shifts_json.append(jsoned_shifts)
        slot_id_to_constraints_dict[slot.id] = slot.constraints
    shifts_json.append(json.dumps(slot_id_to_constraints_dict))
    logger.debug('jsoned shifts are %s' % shifts_json)
    return JsonResponse(shifts_json, safe=False)
