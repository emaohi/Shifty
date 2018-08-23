import datetime
import logging

import pytz
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from health_check.views import MainView
from kombu.exceptions import OperationalError

from core.date_utils import get_current_week_string, get_current_deadline_date_string, \
    get_current_week_range, get_curr_week_sunday, get_next_week_sunday
from core.models import ShiftRequest, ShiftSwap
from core.utils import get_employee_requests_with_status
from log.forms import ManagerSignUpForm, BusinessRegistrationForm, BusinessEditForm, AddEmployeesForm, EditProfileForm
from log.models import EmployeeProfile, Business

from Shifty.utils import must_be_manager_callback, get_curr_profile, get_curr_business, must_be_employee_callback, \
    get_logo_conf, get_profile_and_business, EmailWaitError, must_be_superuser_callback, send_multiple_mails_with_html
from log.utils import NewEmployeeHandler, send_new_employees_mails

logger = logging.getLogger(__name__)


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def manager_home(request):

    curr_manager = request.user.profile

    pending_requests_cnt = get_employee_requests_with_status(curr_manager, 'P').count()

    curr_week_string = get_current_week_string()
    next_week_sunday = get_next_week_sunday()

    deadline_date = get_current_deadline_date_string(curr_manager.business.deadline_day)
    logger.info('deadline date is %s', deadline_date)

    is_finish_slots = curr_manager.business.slot_request_enabled
    logger.info('are slot adding is finished? %s', is_finish_slots)

    context = {'requests_cnt': pending_requests_cnt,
               'curr_week_str': curr_week_string, 'start_date': next_week_sunday,
               'current_start_date': get_curr_week_sunday(),
               'deadline_date': deadline_date, 'shifts_generated': get_curr_business(request).shifts_generated,
               'logo_conf': get_logo_conf()}
    return render(request, "manager/home.html", context)


@login_required(login_url="/login")
@user_passes_test(must_be_employee_callback, login_url='/')
def emp_home(request):
    profile, business = get_profile_and_business(request)

    start_week, end_week = get_current_week_range()
    existing_request = ShiftRequest.objects.filter(employee=get_curr_profile(request),
                                                   submission_time__range=[start_week, end_week]).first()

    deadline_date_str = get_current_deadline_date_string(get_curr_profile(request).business.deadline_day)
    curr_week_string = get_current_week_string()
    curr_week_sunday = get_curr_week_sunday()

    generation_status = business.shifts_generated

    request_enabled = business.slot_request_enabled and deadline_date_str

    is_first_login = False
    if not profile.ever_logged_in:
        logger.info('first login')
        is_first_login = True
        profile.ever_logged_in = True
        profile.save()

    new_messages = get_curr_profile(request).new_messages
    open_swap_requests = ShiftSwap.objects.filter(
        Q(requester=get_curr_profile(request)) | Q(responder=get_curr_profile(request)),
        accept_step__in=ShiftSwap.open_accept_steps()).count()

    return render(request, "employee/home.html", {'got_request_slots': existing_request.requested_slots.all()
                                                  if existing_request else None, 'request_enabled': request_enabled,
                                                  'curr_week_str': curr_week_string,
                                                  'deadline_date': deadline_date_str, 'start_date': curr_week_sunday,
                                                  'first_login': is_first_login, 'generation': generation_status,
                                                  'logo_conf': get_logo_conf(), 'new_messages': new_messages,
                                                  'swap_cnt': open_swap_requests})


def register(request):
    if request.POST:
        manager_form = ManagerSignUpForm(request.POST)
        business_form = BusinessRegistrationForm(request.POST, request.FILES)
        if manager_form.is_valid() and business_form.is_valid():

            manager = manager_form.save()

            logger.info('creating business')

            business = business_form.save(commit=False)

            logo_url = business_form.cleaned_data['logo_url']
            if logo_url:
                logger.info('logo_url is --- %s', logo_url)
                business.save_logo_from_url(logo_url)
            business.manager = manager
            business.save()

            manager.profile.business = business
            manager.profile.role = 'MA'

            logger.info('creating manager profile')
            manager.profile.save()

            # add manager to managers group
            logger.info('adding new manager to the manager group')
            Group.objects.get(name='Managers').user_set.add(manager)

            manager.save()

            user = authenticate(username=manager.username, password=manager_form.cleaned_data.get('password1'))
            login(request, user)
            return HttpResponseRedirect('/success')
        else:
            logger.error('manager form or business form are not valid: %s +++ %s',
                         manager_form.errors, business_form.errors)
    else:
        manager_form = ManagerSignUpForm()
        business_form = BusinessRegistrationForm()

    return render(request, 'manager/register.html', {'manager_form': manager_form, 'business_form': business_form})


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def success(request):
    return render(request, 'manager/register_success.html')


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def edit_business(request):

    curr_business = request.user.profile.business
    if request.POST:

        logger.info('editing business')

        business_form = BusinessEditForm(request.POST, request.FILES, instance=curr_business)
        if business_form.is_valid():

            business = business_form.save()
            business.manager = request.user
            business.save()

            messages.success(request, 'Edited business successfully')
            return HttpResponseRedirect('/')
        else:
            logger.error('edit business form invalid')
            print business_form.errors
    else:
        business_form = BusinessEditForm(instance=curr_business)

    return render(request, 'manager/edit_business.html', {'business_form': business_form})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback, login_url='/employee')
def add_employees(request):
    if request.method == 'POST':
        # get the number of fields (minus the csrf token) and divide by 5 as every user has 5 fields
        num_of_employees = (len(request.POST) - 1) / 5
        form = AddEmployeesForm(request.POST, extra=num_of_employees)

        if form.is_valid():

            data = form.cleaned_data
            curr_business = request.user.profile.business
            mail_dics = []

            logger.info('Going to create %d employees', num_of_employees)
            for i in range(num_of_employees):
                new_employee_handler = NewEmployeeHandler(data['employee_%s_firstName' % str(i)],
                                                          data['employee_%s_lastName' % str(i)],
                                                          data['employee_%s_email' % str(i)],
                                                          data['employee_%s_role' % str(i)],
                                                          data['employee_%s_dateJoined' % str(i)],
                                                          request.user)
                logger.info('creating employee')
                new_employee = new_employee_handler.create_employee()
                # add employee to employees group
                logger.info('adding employee to Employee group')
                Group.objects.get(name='Employees').user_set.add(new_employee)

                mail_dics.append(new_employee_handler.get_invitation_mail_details())

            try:
                logger.info('sending mails to new employees')
                send_new_employees_mails(mail_dics)
                messages.success(request, 'successfully added %s employees to %s' % (str(num_of_employees),
                                                                                     curr_business))
            except (OperationalError, EmailWaitError) as e:
                logger.error('sending emails failed ' + str(e.message))
                messages.error(request, 'failed to send mails to employees')

            return HttpResponseRedirect('/')
    else:
        form = AddEmployeesForm()
    return render(request, "manager/add_employees.html", {'form': form, 'logo_conf': get_logo_conf()})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def manage_employees(request):
    curr_business = request.user.profile.business

    logger.info('getting business employees')
    all_employees = EmployeeProfile.objects.filter(business=curr_business).select_related('user')
    paginator = Paginator(all_employees, 10)

    page = request.GET.get('page', 1)
    try:
        page_employees = paginator.page(page)
    except PageNotAnInteger:
        page_employees = paginator.page(1)
    except EmptyPage:
        page_employees = paginator.page(paginator.num_pages)

    return render(request, 'manager/manage_employees.html',
                  {'employees': page_employees, 'curr_business': curr_business, 'logo_conf': get_logo_conf()})


@login_required(login_url='/login')
def edit_profile_form(request):
    if request.method == 'GET':
        employee_username = request.GET.get('username', None)
        is_manager = request.user.groups.filter(name='Managers').exists()
        if not is_manager:
            logger.info('employee profile - creating employee edit profile form')
            initial_form = EditProfileForm(instance=request.user.profile, is_manager=False)
        else:
            logger.info('manager profile - creating manager edit profile form')
            initial_form = EditProfileForm(instance=EmployeeProfile.objects.get(user__username=employee_username if
                                                                                employee_username else
                                                                                request.user.username),
                                           is_manager=True)
        return render(request, 'ajax_form.html', {'form': initial_form})
    else:
        profile = EmployeeProfile.objects.get(user=request.POST.get('user'))
        is_manager = request.user.groups.filter(name='Managers').exists()
        form = EditProfileForm(request.POST, instance=profile, is_manager=is_manager)
        if form.is_valid():
            edited_profile = form.save()
            is_edited_other = is_manager and request.user.profile != edited_profile
            messages.success(request, message='successfully edited %s' %
                                              (edited_profile.user.username if is_edited_other else 'yourself'))
            logger.info('going to delete cached ETA duration...')
            cache.delete(get_curr_profile(request).get_eta_cache_key())
            return redirect('manage_employees' if is_edited_other else 'edit_profile')
        else:
            logger.error(str(form.errors))
            messages.error(request, message='couldn\'t edit profile: %s' % str(form.errors.as_text()))
            return redirect('/')


@login_required(login_url='/login')
def edit_profile(request):
    return render(request, 'edit_profile.html', {'employee': request.user.username})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def delete_user(request):
    username = request.POST.get('username')
    user_to_delete = User.objects.get(username=username)

    user_to_delete.delete()
    logger.info('successfully deleted user')
    messages.success(request, message='successfully deleted %s' % username)
    return HttpResponse('ok')


def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.groups.filter(name="Managers").exists():
        # user is a manager
        return redirect("manager_home")
    else:
        return redirect("emp_home")


def home_or_login(request):
    """
    Redirects users based on whether they are authenticated
    """
    if request.user.is_authenticated():
        # user is a manager
        return redirect("login_success")
    else:
        return redirect("login")


def ask_join_business(request):

    if request.user.is_authenticated:
        return HttpResponseBadRequest('Dude you are already part of the system :)')

    seconds_to_expiry = None
    session = request.session
    if Session.objects.filter(pk=session.session_key).exists():
        session_expire_date = Session.objects.get(pk=session.session_key).expire_date
        seconds_to_expiry = (session_expire_date.replace(tzinfo=None) - datetime.datetime.utcnow()).seconds

    if session.get('has_asked', False):
        logger.info('already asked... session id: %s, expire date: %s', session.session_key, seconds_to_expiry)
        return HttpResponse("You've already asked, Try again in %s seconds..." % seconds_to_expiry)
    else:
        logger.debug('setting expiry for the anonymous session id %s', session.session_key)
        session.set_expiry(300)

    emp_name = request.GET.get('username')
    business_name = request.GET.get('business')
    business = Business.objects.filter(business_name=business_name).first()

    if not business:
        session['has_asked'] = True
        return HttpResponse('No such business....')

    send_multiple_mails_with_html(subject='New message in Shifty app',
                                  text='you\'ve got new message from %s anonymous user' % emp_name,
                                  template='html_msgs/ask_join.html',
                                  r_2_c_dict={business.get_manager().user:
                                              {'manager_name': business.get_manager().user.username,
                                               'emp_name': emp_name,
                                               'business_name': business.business_name}},
                                  wait_for_results=False)
    request.session['has_asked'] = True
    return HttpResponse('Thanks for asking! You will be in touch in case your manager approves')


class HealthCheckCustomView(MainView):
    @method_decorator(user_passes_test(must_be_superuser_callback, redirect_field_name=None))
    def dispatch(self, request, *args, **kwargs):
        return super(HealthCheckCustomView, self).dispatch(request, *args, **kwargs)
