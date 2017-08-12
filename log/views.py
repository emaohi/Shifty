import traceback

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

from core.date_utils import get_current_week_string, get_next_week_string, get_current_deadline_date
from core.utils import *
from forms import *
from log.models import EmployeeProfile
from utils import *

from Shifty.utils import must_be_manager_callback

logger = logging.getLogger('cool')


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def manager_home(request):

    curr_manager = request.user.profile

    pending_emp_requests = get_employee_requests_with_status(curr_manager, 'P')

    approved_emp_requests = get_employee_requests_with_status(curr_manager, 'A')
    rejected_emp_requests = get_employee_requests_with_status(curr_manager, 'R')

    done_emp_requests = approved_emp_requests.union(rejected_emp_requests).order_by('-sent_time')

    curr_week_string = get_current_week_string()
    next_week_date = get_next_week_string().split(' --')[0].replace('/', '-')
    logger.info(next_week_date)

    deadline_date = get_current_deadline_date(curr_manager.business.deadline_day)
    logger.info('deadline date is %s' % deadline_date)

    context = {'pending_requests': pending_emp_requests, 'done_requests': done_emp_requests,
               'curr_week_str': curr_week_string, 'start_date': next_week_date,
               'deadline_date': deadline_date}
    return render(request, "manager/home.html", context)


@login_required(login_url="/login")
@user_passes_test(lambda user: user.groups.filter(name='Employees').exists(), login_url='/')
def emp_home(request):
    manager_messages = get_manger_msgs_of_employee(request.user.profile)
    return render(request, "employee/home.html", {'manager_msgs': manager_messages})


def register(request):
    if request.POST:
        manager_form = ManagerSignUpForm(request.POST)
        business_form = BusinessRegistrationForm(request.POST)
        if manager_form.is_valid() and business_form.is_valid():

            manager = manager_form.save()

            logger.info('creating business')
            business = business_form.save()
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
            logger.error('manager form or business form are not valid')
            print manager_form.error_messages
            print business_form.errors
    else:
        manager_form = ManagerSignUpForm()
        business_form = BusinessRegistrationForm()

    return render(request, 'manager/register.html', {'manager_form': manager_form, 'business_form': business_form})


@login_required
def success(request):
    return render(request, 'manager/register_success.html')


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def edit_business(request):

    curr_business = request.user.profile.business
    if request.POST:

        logger.info('editing business')

        business_form = BusinessEditForm(request.POST, instance=curr_business)
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
        # get the number of fields (minus the csrf token) and divide by 4 as every user has 4 fields
        num_of_employees = (len(request.POST) - 1) / 5
        form = AddEmployeesForm(request.POST, extra=num_of_employees)

        if form.is_valid():

            data = form.cleaned_data
            curr_business = request.user.profile.business
            mail_dics = []
            new_employee_handler = None

            logger.info('Going to create %d employees' % num_of_employees)
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
                new_employee_handler.send_new_employees_mails(mail_dics)
                messages.success(request, 'successfully added %s employees to %s' % (str(num_of_employees),
                                                                                     curr_business))
            except Exception as e:
                logger.error('sending emails failed ' + str(e.message) + str(traceback.format_exc()))
                messages.error(request, 'failed to send mails to employees')

            return HttpResponseRedirect('/')
    else:
        form = AddEmployeesForm()
    return render(request, "manager/add_employees.html", {'form': form})


@login_required(login_url='/login')
@user_passes_test(must_be_manager_callback)
def manage_employees(request):
    curr_business = request.user.profile.business

    logger.info('getting business employees')
    all_employees = EmployeeProfile.objects.filter(business=curr_business)

    return render(request, 'manager/manage_employees.html',
                  {'employees': all_employees, 'curr_business': curr_business})


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
            return redirect('manage_employees' if is_edited_other else 'edit_profile')
        else:
            logger.error(str(form.errors))
            messages.error(request, message='couldn\'t edit profile: %s' % str(form.errors.as_text()))
            return redirect('manage_employees')


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
