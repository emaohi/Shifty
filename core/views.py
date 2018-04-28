import csv
import json
import logging
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse, \
    HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_POST, require_GET

from core.date_utils import get_next_week_string, get_curr_year, get_next_week_num, \
    get_days_hours_from_delta, get_curr_week_num, get_current_week_range
from core.forms import BroadcastMessageForm, ShiftSlotForm, SelectSlotsForm, ShiftSummaryForm
from core.models import EmployeeRequest, ShiftSlot, ShiftRequest, Shift, ShiftSwap, SavedSlot
from core.utils import create_manager_msg, get_holiday, save_shifts_request, \
    NoLogoFoundError, get_employee_requests_with_status, \
    SlotCreator, SlotConstraintCreator, DurationApiClient, LogoUrlFinder, LanguageValidator

from Shifty.utils import must_be_manager_callback, EmailWaitError, must_be_employee_callback, get_curr_profile, \
    get_curr_business, wrong_method, get_logo_conf
from core import tasks
from log.models import EmployeeProfile

logger = logging.getLogger(__name__)


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback, login_url='/manager')
def report_incorrect_detail(request):
    if request.method == 'POST':
        reporting_profile = get_curr_profile(request)
        incorrect_field = request.POST.get('incorrect_field')
        fix_suggestion = request.POST.get('fix_suggestion')
        curr_val = request.POST.get('curr_val')
        language_validator = LanguageValidator(settings.PROFANITY_SERVICE_URL)

        logger.info('checking language')
        if not language_validator.validate(fix_suggestion):
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
            get_curr_profile(request).send_mail_to_manager()
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
    else:  # method is GET
        form = BroadcastMessageForm()
        return render(request, 'ajax_form.html', {'form': form})


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback)
@require_GET
def get_manager_messages(request):
    curr_emp_profile = get_curr_profile(request)
    is_new_str = request.GET.get('new')
    is_new = True if is_new_str == 'true' else False
    manager_messages = curr_emp_profile.get_manger_msgs_of_employee(is_new)

    logger.debug('flushing new messages cache for emp %s', str(curr_emp_profile))
    curr_emp_profile.flush_new_messages()

    return render(request, "employee/manager_messages.html", {'manager_msgs': manager_messages, 'is_new': is_new})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
@require_GET
def get_employee_requests(request):
    curr_manager = get_curr_profile(request)
    is_pending_str = request.GET.get('pending')
    is_pending = True if is_pending_str == 'true' else False
    if is_pending:
        emp_requests = get_employee_requests_with_status(curr_manager, 'P')
    else:
        key = curr_manager.get_old_employee_requests_cache_key()
        if key not in cache:
            logger.debug('Taking old employee requests from DB: %s', messages)
            emp_requests = get_employee_requests_with_status(curr_manager, 'A', 'R')
            cache.set(key, list(emp_requests), settings.DURATION_CACHE_TTL)
        else:
            logger.debug('Taking old employee requests from cache')
            emp_requests = cache.get(key)

    return render(request, 'manager/emp_requests.html', {'requests': emp_requests, 'is_pending': is_pending})


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
            constraint_creator = SlotConstraintCreator(data)
            slot_creator = SlotCreator(business, data, constraint_creator)

            try:
                slot_creator.create()
                messages.success(request, 'slot form was ok')
                return HttpResponseRedirect('/')
            except ObjectDoesNotExist as e:
                logger.error('object does not exist: %s', e)
                return HttpResponseBadRequest('object does not exist: %s' % str(e))
        else:
            day = request.POST.get('day')
            slot_holiday = get_holiday(get_curr_year(), day, get_next_week_num())
            return render(request, 'manager/new_shift.html', {'form': slot_form, 'week_range': get_next_week_string(),
                                                              'holiday': slot_holiday}, status=400)
    else:
        day = request.GET.get('day', '')
        start_hour = request.GET.get('startTime', '')

        slot_holiday = get_holiday(get_curr_year(), day, get_next_week_num())

        form = ShiftSlotForm(initial={'day': day, 'start_hour': start_hour.replace('-', ':')}, business=business,
                             names=((name[0], name[0]) for name in
                                    SavedSlot.objects.exclude(name__startswith='Custom').values_list('name')))

        return render(request, 'manager/new_shift.html', {'form': form, 'week_range': get_next_week_string(),
                                                          'holiday': slot_holiday, 'logo_conf': get_logo_conf()})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
@require_GET
def saved_slot_exist(request, slot_name):
    curr_business = get_curr_business(request)
    if SavedSlot.objects.filter(name=slot_name, shiftslot__business=curr_business).exists():
        return HttpResponse('')
    return HttpResponseNotFound('')


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
            slot_constraint_json = SlotConstraintCreator(data).create()

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
                                                             'id': slot_id, 'holiday': updated_slot.holiday,
                                                             'logo_conf': get_logo_conf()})


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

    next_week_slots = ShiftSlot.objects.filter(week=get_next_week_num(), business=get_curr_business(request))
    for slot in next_week_slots:
        text_color, title = slot.get_color_and_title()
        jsoned_shift = json.dumps({'id': str(slot.id), 'title': title,
                                   'start': slot.start_time_str(),
                                   'end': slot.end_time_str(),
                                   'backgroundColor': '#205067' if not slot.was_shift_generated() else 'blue',
                                   'textColor': text_color})
        shifts_json.append(jsoned_shift)
        slot_id_to_constraints_dict[slot.id] = slot.constraints
    shifts_json.append(json.dumps(slot_id_to_constraints_dict))
    logger.debug('jsoned shifts are %s', shifts_json)
    return JsonResponse(shifts_json, safe=False)


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback, login_url='/manager')
def submit_slots_request(request):
    next_week_no = get_next_week_num()
    curr_business = get_curr_business(request)
    curr_profile = get_curr_profile(request)
    start_week, end_week = get_current_week_range()
    existing_request = ShiftRequest.objects.filter(employee=curr_profile,
                                                   submission_time__range=[start_week, end_week]).last()
    if request.method == 'GET':
        form = SelectSlotsForm(instance=existing_request, business=curr_business,
                               week=next_week_no)
        existing_slots = existing_request.requested_slots.all() if existing_request else []
        request_enabled = curr_business.slot_request_enabled
        return render(request, 'employee/slot_list.html', {'form': form, 'existing_slots': existing_slots,
                                                           'request_enabled': request_enabled})
    else:
        form = SelectSlotsForm(request.POST, business=curr_business, week=next_week_no, instance=existing_request)
        if form.is_valid():
            shifts_request = save_shifts_request(form, curr_profile)

            logger.info('slots chosen are: %s', str(shifts_request.requested_slots.all()))
            messages.success(request, 'request saved')
        else:
            logger.error('couldn\'t save slots request: %s', str(form.errors.as_text()))
            messages.error(request, message='couldn\'t save slots request: %s' % str(form.errors.as_text()))
        return HttpResponseRedirect('/')


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


@login_required(login_url='/login')
def get_work_duration_data(request):
    if request.method == 'GET':
        curr_profile = get_curr_profile(request)
        curr_business = get_curr_business(request)
        key = curr_profile.get_eta_cache_key()

        if key not in cache:
            home_address = curr_profile.home_address
            work_address = curr_business.address
            arrival_method = curr_profile.arriving_method
            duration_client = DurationApiClient(home_address, work_address)

            if not home_address or not work_address:
                return HttpResponseBadRequest('can\'t get distance data - work address or home address are not set')

            driving_duration, walking_duration = duration_client.get_dist_data(arrival_method)

            if not walking_duration and not driving_duration:
                return HttpResponseBadRequest('cant find home to work durations - make sure both business'
                                              'and home addresses are available')
            cache.set(key, (driving_duration, walking_duration), settings.DURATION_CACHE_TTL)
        else:
            driving_duration, walking_duration = cache.get(key)

        logger.info('found distance data: driving duration is %s and walking duration is %s',
                    driving_duration, walking_duration)
        return JsonResponse({'driving': driving_duration, 'walking': walking_duration})

    return HttpResponseBadRequest('cannot get distance data with ' + request.method)


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def get_slot_request_employees(request, slot_id):
    if request.method == 'GET':
        requested_slot = ShiftSlot.objects.get(id=slot_id)
        if not requested_slot.is_next_week():
            return HttpResponseBadRequest('slot is not next week')

        slot_requests = ShiftRequest.objects.filter(requested_slots=requested_slot)

        return render(request, 'slot_request_emp_list.html',
                      {'emps': [req.employee for req in slot_requests],
                       'empty_msg': 'No employees chose this slot'})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def generate_shifts(request):
    def execute_shift_generation(business):

        business.set_shift_generation_pending()
        business.save()

        if settings.CELERY:
            tasks.generate_next_week_shifts.delay(business.business_name, settings.SHIFT_GENERATION_ALGORITHM_LEVEL)
        else:
            tasks.generate_next_week_shifts(business.business_name, settings.SHIFT_GENERATION_ALGORITHM_LEVEL)

    if request.method == 'POST':
        next_week_slots = ShiftSlot.objects.filter(week=get_next_week_num(), business=get_curr_business(request))
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
        curr_employee = get_curr_profile(request)
        requested_slot = ShiftSlot.objects.get(id=slot_id)
        if requested_slot.was_shift_generated():
            shift = requested_slot.shift
            curr_emp_future_slots = curr_employee.get_current_week_slots()
            offer_swap = (len(curr_emp_future_slots) > 0) and (not get_curr_profile(request) in shift.employees.all())
            return render(request, 'slot_request_emp_list.html',
                          {'emps': shift.employees.all(), 'empty_msg': 'No employees in this shift :(',
                           'curr_emp': get_curr_profile(request),
                           'future_slots': curr_emp_future_slots, 'offer_swap': offer_swap})
        else:
            logger.warning('Can\'t get employees for slot id %s, shift was not generated', slot_id)
            return HttpResponse('Cant find shift for this slot')

    return wrong_method(request)


@login_required(login_url='/login')
def get_calendar_current_week_shifts(request):
    if request.method == 'GET':
        shifts_json = []

        current_week_slots = ShiftSlot.objects.filter(week=get_curr_week_num(),
                                                      business=get_curr_business(request))

        for slot in current_week_slots:
            if not slot.was_shift_generated():
                continue

            bg_color, text_color = slot.get_calendar_colors(get_curr_profile(request))

            jsoned_shift = json.dumps({'id': str(slot.id), 'title': slot.name,
                                       'start': slot.start_time_str(),
                                       'end': slot.end_time_str(),
                                       'backgroundColor': bg_color,
                                       'textColor': text_color})
            shifts_json.append(jsoned_shift)
        return JsonResponse(json.dumps(shifts_json), safe=False)

    return wrong_method(request)


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def submit_shift_summary(request, slot_id):
    shift = Shift.objects.get(slot=ShiftSlot.objects.get(pk=slot_id))
    if request.method == 'POST':
        summary_form = ShiftSummaryForm(request.POST, id=slot_id, instance=shift)
        if summary_form.is_valid():
            summary_form.save()
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


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback)
@require_GET
def get_time_to_next_shift(request):
    curr_emp = get_curr_profile(request)
    next_shift = curr_emp.get_next_shift()
    if not next_shift:
        logger.warning('no upcoming shift for emp %s', request.user.username)
        return HttpResponseBadRequest('No upcoming shift was found...')
    logger.info('next shift for user %s is %s', request.user.username, str(next_shift))
    days, hours = get_days_hours_from_delta(next_shift.slot.get_datetime() - datetime.now())

    return HttpResponse('%s days, %s hours' % (days, hours))


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback)
@require_GET
def get_prev_shifts(request):
    curr_emp = get_curr_profile(request)
    prev_shifts = curr_emp.get_previous_shifts()
    if len(prev_shifts) == 0:
        logger.warning('no previous shifts for emp %s', request.user.username)
        return HttpResponseBadRequest('No previous shifts was found...')
    logger.info('Found %d previous shifts for user %s', len(prev_shifts), request.user.username)

    return render(request, 'employee/previous_shifts.html', {'prev_shifts': prev_shifts})


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback)
def export_shifts_csv(request):
    curr_emp = get_curr_profile(request)
    prev_shifts = curr_emp.get_previous_shifts()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="prev_shifts.csv"'

    writer = csv.writer(response)
    writer.writerow(['shift date', 'tip'])
    for shift in prev_shifts:
        writer.writerow([shift.slot.get_datetime_str(), shift.calculate_employee_tip()])

    return response


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
@require_GET
def get_logo_suggestion(request):
    business_name = request.GET.get('name', '')
    logo_finder = LogoUrlFinder(settings.LOGO_LOOKUP_URL)
    try:
        logo_url = logo_finder.find_logo(business_name)
    except NoLogoFoundError as e:
        logger.warning('couldn\'t found url for name: %s', business_name)
        return HttpResponseBadRequest('Couldn\'t find logo... %s' % e.message)

    logger.info('found url: %s', logo_url)
    return JsonResponse({'logo_url': logo_url})


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback)
@require_POST
def ask_shift_swap(request):
    try:
        responder = EmployeeProfile.objects.get(user__username=request.POST.get('requested_employee'))
        requested_shift = ShiftSlot.objects.get(id=int(request.POST.get('requested_shift'))).shift
        requester_shift = ShiftSlot.objects.get(id=int(request.POST.get('requester_shift'))).shift
        logger.info('new swap request for shift %d to shift %d', requester_shift.id, requested_shift.id)

        ShiftSwap.objects.create(requester=get_curr_profile(request), responder=responder,
                                 requested_shift=requested_shift,
                                 requester_shift=requester_shift)
        return HttpResponse('ok')
    except (ValueError, IntegrityError) as e:
        return HttpResponseBadRequest('bad request: %s' % e.message)


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback)
@require_GET
def get_swap_requests(request):
    curr_employee = get_curr_profile(request)
    is_open = True if request.GET.get('state') == 'open' else False
    if is_open:
        swap_requests = ShiftSwap.objects.filter(
            Q(requester=curr_employee) | Q(responder=curr_employee),
            accept_step__in=ShiftSwap.open_accept_steps()).order_by('-updated_at')
    else:
        key = curr_employee.get_old_swap_requests_cache_key()
        if key not in cache:
            swap_requests = ShiftSwap.objects.filter(
                Q(requester=curr_employee) | Q(responder=curr_employee),
                accept_step__in=ShiftSwap.closed_accept_steps()).order_by('-updated_at')
            cache.set(key, list(swap_requests), settings.DURATION_CACHE_TTL)
            logger.debug('Taking old swap requests from DB: %s', swap_requests)

        logger.debug('Taking old swap requests from cache')
        swap_requests = cache.get(key)

    return render(request, 'employee/swap_requests.html', {'swap_requests': swap_requests, 'is_open': is_open})


@login_required(login_url='/login')
@user_passes_test(must_be_employee_callback)
@require_POST
def respond_swap_request(request):
    try:
        swap_request = ShiftSwap.objects.get(pk=request.POST.get('emp_request_id'))
        logger.debug('swap request id is %s', swap_request)
        is_accept = request.POST.get('is_accept') == 'true'
        swap_request.accept_step = 1 if is_accept else -1
        logger.info('saving %s : %s...', swap_request, 'accept' if is_accept else 'reject')
        swap_request.save()
        return HttpResponse('ok')
    except KeyError as e:
        return HttpResponseBadRequest('Bad request: ' + str(e))
