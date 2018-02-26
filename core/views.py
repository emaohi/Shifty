import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse, \
    HttpResponseBadRequest
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from core.date_utils import get_next_week_string, get_curr_year, get_next_week_num, get_curr_week_num
from core.forms import BroadcastMessageForm, ShiftSlotForm, SelectSlotsForm, ShiftSummaryForm
from core.models import EmployeeRequest, ShiftSlot, ShiftRequest, Shift
from core.utils import create_manager_msg, send_mail_to_manager, create_constraint_json_from_form, get_holiday_or_none, \
    get_color_and_title_from_slot, duplicate_favorite_slot, handle_named_slot, get_dist_data, parse_duration_data, \
    save_shifts_request, delete_other_requests, validate_language, get_week_slots

from Shifty.utils import must_be_manager_callback, EmailWaitError, must_be_employee_callback, get_curr_profile, \
    get_curr_business, wrong_method
from core import tasks

logger = logging.getLogger(__name__)


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback, login_url='/manager')
def report_incorrect_detail(request):
    if request.method == 'POST':
        reporting_profile = get_curr_profile(request)
        incorrect_field = request.POST.get('incorrect_field')
        fix_suggestion = request.POST.get('fix_suggestion')
        curr_val = request.POST.get('curr_val')

        logger.info('checking language')
        if not validate_language(fix_suggestion):
            logger.info('bad language detected')
            return HttpResponseBadRequest('NOT SENT - BAD LANGUAGE')

        logger.info('msg OK, creating new employee request')
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
            recipients = get_curr_business(request).get_employees()

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
            messages.error(request, message='couldn\'t send broadcast message: %s' % str(form.errors.as_text()))
            return HttpResponseRedirect('/')
    else:    # method is GET
        form = BroadcastMessageForm()
        return render(request, 'ajax_form.html', {'form': form})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def add_shift_slot(request):

    business = get_curr_business(request)
    slot_names = [t['name'] for t in ShiftSlot.objects.filter(business=business)
                  .values('name').distinct() if t['name'] != 'Custom']

    if request.method == 'POST':

        slot_form = ShiftSlotForm(request.POST, business=business, names=((name, name) for name in slot_names))
        if slot_form.is_valid():
            data = slot_form.cleaned_data
            day = data['day']
            start_hour = data['start_hour']
            end_hour = data['end_hour']

            if data['name'] == '':
                name = data.get('save_as', None)

                slot_constraint_json = create_constraint_json_from_form(data)

                slot_holiday = get_holiday_or_none(get_curr_year(), data['day'], get_next_week_num())

                new_slot = ShiftSlot(business=request.user.profile.business, day=day,
                                     start_hour=start_hour, end_hour=end_hour,
                                     constraints=json.dumps(slot_constraint_json),
                                     week=get_next_week_num(), holiday=slot_holiday, is_mandatory=data['mandatory'])
                if name:
                    new_slot.name = name
                new_slot.save()

                if name and name != 'Custom':
                    handle_named_slot(business, name)
            else:
                new_name = data['name']
                cloned_slot = duplicate_favorite_slot(business, new_name)
                ShiftSlot.objects.filter(id=cloned_slot.id).update(day=day, week=get_next_week_num(),
                                                                   start_hour=start_hour, end_hour=end_hour)
            messages.success(request, 'slot form was ok')
            return HttpResponseRedirect('/')
        else:
            day = request.POST.get('day')
            slot_holiday = get_holiday_or_none(get_curr_year(), day, get_next_week_num())
            return render(request, 'manager/new_shift.html', {'form': slot_form, 'week_range': get_next_week_string(),
                                                              'holiday': slot_holiday}, status=400)
    else:
        day = request.GET.get('day', '')
        start_hour = request.GET.get('startTime', '')

        slot_holiday = get_holiday_or_none(get_curr_year(), day, get_next_week_num())

        form = ShiftSlotForm(initial={'day': day, 'start_hour': start_hour.replace('-', ':')}, business=business,
                             names=((name, name) for name in slot_names))
        return render(request, 'manager/new_shift.html', {'form': form, 'week_range': get_next_week_string(),
                                                          'holiday': slot_holiday})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def update_shift_slot(request, slot_id):

    updated_slot = get_object_or_404(ShiftSlot, id=slot_id)

    if not updated_slot.is_next_week():
        return HttpResponseBadRequest('<h3>this shift is not at next week</h3>')

    business = request.user.profile.business

    if request.method == 'POST':
        logger.info('in post, is is %s', slot_id)
        slot_form = ShiftSlotForm(request.POST, business=business)
        if slot_form.is_valid():
            data = slot_form.cleaned_data
            slot_constraint_json = create_constraint_json_from_form(data)

            logger.info('new end hour is %s', str(data['end_hour']))
            ShiftSlot.objects.filter(id=slot_id).update(business=request.user.profile.business, day=data['day'],
                                                        start_hour=data['start_hour'], end_hour=data['end_hour'],
                                                        constraints=json.dumps(slot_constraint_json),
                                                        is_mandatory=data['mandatory'])
            messages.success(request, 'slot updated')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'manager/new_shift.html', {'form': slot_form})
    else:  # GET
        logger.info('in get, ID is %s', slot_id)
        day = int(updated_slot.day)
        start_hour = str(updated_slot.start_hour)
        end_hour = str(updated_slot.end_hour)
        is_mandatory = updated_slot.is_mandatory
        form = ShiftSlotForm(initial={'day': day, 'start_hour': start_hour.replace('-', ':'),
                                      'end_hour': end_hour.replace('-', ':'), 'mandatory': is_mandatory},
                             business=business)
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
        logger.info('shift slow id %s was deleted', slot_id)
        messages.success(request, 'slot was deleted successfully')
        return HttpResponse('ok')

    return HttpResponseBadRequest('cannot delete with GET')


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def get_next_week_slots_calendar(request):
    shifts_json = []
    slot_id_to_constraints_dict = {}
    slot_id_to_generated_status_dict = {}

    next_week_slots = get_week_slots(get_curr_business(request), get_next_week_num())
    for slot in next_week_slots:
        text_color, title = get_color_and_title_from_slot(slot)
        jsoned_shift = json.dumps({'id': str(slot.id), 'title': title,
                                   'start': slot.start_time_str(),
                                   'end': slot.end_time_str(),
                                   'backgroundColor': '#205067' if not slot.was_shift_generated() else 'blue',
                                   'textColor': text_color})
        shifts_json.append(jsoned_shift)
        slot_id_to_constraints_dict[slot.id] = slot.constraints
        slot_id_to_generated_status_dict[slot.id] = slot.was_shift_generated()
    shifts_json.append(json.dumps(slot_id_to_constraints_dict))
    shifts_json.append(json.dumps(slot_id_to_generated_status_dict))
    logger.debug('jsoned shifts are %s', shifts_json)
    return JsonResponse(shifts_json, safe=False)


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback, login_url='/manager')
def submit_slots_request(request):
    next_week_no = get_next_week_num()
    curr_business = get_curr_business(request)
    if request.method == 'GET':
        form = SelectSlotsForm(business=curr_business, week=next_week_no)
        return render(request, 'employee/slot_list.html', {'form': form})
    else:
        form = SelectSlotsForm(request.POST, business=curr_business, week=next_week_no)
        if form.is_valid():
            shifts_request = save_shifts_request(form, request)
            delete_other_requests(request, shifts_request)

            logger.info('slots chosen are: %s', str(shifts_request.requested_slots.all()))
            messages.success(request, 'request saved')
            return HttpResponseRedirect('/')
        else:
            logger.error('couldn\'t save slots request: %s', str(form.errors.as_text()))
            messages.error(request, message='couldn\'t save slots request: %s' % str(form.errors.as_text()))
            return render(request, 'employee/home.html', {'form': form})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def is_finish_slots(request):
    curr_business = get_curr_business(request)
    if request.method == 'POST':
        action = request.POST.get('isFinished')
        curr_business.slot_request_enabled = True if action == 'true' else False
        curr_business.save()

        recp = curr_business.get_employees()
        is_enabled = 'enabled' if curr_business.slot_request_enabled else 'disabled'
        text = 'Your manager has %s shifts requests for next week.' % is_enabled
        create_manager_msg(recipients=recp, subject='Shift requests are now %s' % is_enabled, text=text,
                           wait_for_mail_results=False)

        logger.info('saved business finished slots status to: %s', curr_business.slot_request_enabled)
        return HttpResponse('ok')
    logger.info('returning the business finished slots status which is: %s', curr_business.slot_request_enabled)
    return HttpResponse(curr_business.slot_request_enabled)


@cache_page(60 * 15, key_prefix='shifty')
@vary_on_cookie
@login_required(login_url='/login')
def get_work_duration_data(request):
    if request.method == 'GET':
        home_address = request.user.profile.home_address
        work_address = request.user.profile.business.address

        if not home_address or not work_address:
            return HttpResponseBadRequest('can\'t get distance data - work address or home address are not set')

        is_walk = request.GET.get('walking', True)
        is_drive = request.GET.get('driving', True)

        distance_data = get_dist_data(home_address, work_address, is_drive, is_walk)

        parse_duration_data(distance_data)
        if not distance_data['walking'] and not distance_data['driving']:
            return HttpResponseBadRequest('cant find home to work durations - make sure both business'
                                          'and home addresses are available')

        logger.info('found distance data: ' + str(distance_data))
        return JsonResponse(distance_data)

    return HttpResponseBadRequest('cannot get distance data with ' + request.method)


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def get_slot_request_employees(request, slot_id):
    if request.method == 'GET':
        print ShiftSlot.objects.first().id
        requested_slot = ShiftSlot.objects.get(id=slot_id)
        if not requested_slot.is_next_week():
            return HttpResponseBadRequest('slot is not next week')

        slot_requests = ShiftRequest.objects.filter(requested_slots=requested_slot)

        return render(request, 'manager/slot_request_emp_list.html',
                      {'emps': [req.employee for req in slot_requests],
                       'empty_msg': 'No employees chose this slot'})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def generate_shifts(request):
    def execute_shift_generation(business):

        business.set_shift_generation_pending()
        business.save()

        if settings.CELERY:
            tasks.generate_next_week_shifts.delay(business.business_name)
        else:
            tasks.generate_next_week_shifts(business.business_name)

    if request.method == 'POST':
        next_week_slots = get_week_slots(get_curr_business(request), get_next_week_num())
        if not len(next_week_slots):
            messages.error(request, 'No slots next week !')
            return HttpResponseBadRequest('No slots next week !')
        else:
            execute_shift_generation(get_curr_business(request))

            create_manager_msg(recipients=get_curr_business(request).get_employees(),
                               subject='New Shifts', text='Your manager has generated shifts for next week',
                               wait_for_mail_results=False)
            messages.success(request, 'Shifts generation requested successfully')
            return HttpResponse('Request triggered')

    return wrong_method(request)


@login_required(login_url='/login')
def get_slot_employees(request, slot_id):
    if request.method == 'GET':
        requested_slot = ShiftSlot.objects.get(id=slot_id)
        if requested_slot.was_shift_generated():
            shift = requested_slot.shift
            return render(request, 'manager/slot_request_emp_list.html',
                          {'emps': shift.employees.all(), 'empty_msg': 'No employees in this shift :(',
                           'curr_emp': get_curr_profile(request)})
        else:
            logger.error('cant find shift for slot id %s', slot_id)
            return HttpResponse('Cant find shift for this slot')

    return wrong_method(request)


@login_required(login_url='/login')
def get_calendar_current_week_shifts(request):
    if request.method == 'GET':
        shifts_json = []

        current_week_slots = get_week_slots(get_curr_business(request), get_curr_week_num())

        logger.warning('checking sentry')

        for slot in current_week_slots:
            if not slot.was_shift_generated():
                continue
            if get_curr_profile(request).role != 'MA':
                bg_color, text_color = ('mediumseagreen', 'white') if get_curr_profile(request) in\
                    slot.shift.employees.all() else ('#7b8a8b', 'black')
            else:
                bg_color, text_color = 'cornflowerblue', 'white'

            jsoned_shift = json.dumps({'id': str(slot.id), 'title': slot.name,
                                       'start': slot.start_time_str(),
                                       'end': slot.end_time_str(),
                                       'backgroundColor': bg_color,
                                       'textColor': text_color})
            shifts_json.append(jsoned_shift)
        return JsonResponse(json.dumps(shifts_json), safe=False)

    return wrong_method(request)


def submit_shift_summary(request, slot_id):
    shift = Shift.objects.get(slot=ShiftSlot.objects.get(pk=slot_id))
    old_rank = shift.rank
    if request.method == 'POST':
        summary_form = ShiftSummaryForm(request.POST, id=slot_id, instance=shift)
        if summary_form.is_valid():
            summary_form.save()
            shift.update_emp_rates(old_rank)
            messages.success(request, message='Shift summary submitted')
            return HttpResponseRedirect('/')
        else:
            logger.error('Shift summary form is not valid: %s', str(summary_form.errors))
            messages.error(request, message='couldn\'t submit shift summary: %s' % str(summary_form.errors.as_text()))
            return HttpResponseRedirect('/')

    if not shift.slot.is_finished():
        return HttpResponseBadRequest('shift is not over yet...')
    summary_form = ShiftSummaryForm(id=slot_id, instance=shift)
    return render(request, 'manager/shift_summary_form.html', context={'summary_form': summary_form,
                                                                       'slot_id': slot_id})
