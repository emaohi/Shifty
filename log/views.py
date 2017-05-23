import traceback

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

from forms import *
from utils import *

logging.basicConfig(format='%(levelname)s %(asctime)s %(module)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@login_required(login_url="/login")
@user_passes_test(lambda user: user.groups.filter(name='Managers').exists())
def manager_home(request):
    return render(request, "manager/home.html")


@login_required(login_url="/login")
@user_passes_test(lambda user: user.groups.filter(name='Employees').exists(), login_url='/')
def emp_home(request):
    return render(request, "employee/home.html")


def register(request):
    if request.POST:
        manager_form = ManagerSignUpForm(request.POST)
        business_form = BusinessRegistrationForm(request.POST)
        if manager_form.is_valid() and business_form.is_valid():

            manager = manager_form.save()

            business = business_form.save()
            business.manager = manager
            business.save()

            manager.profile.business = business
            manager.profile.role = 'MA'

            manager.profile.save()

            # add manager to managers group
            Group.objects.get(name='Managers').user_set.add(manager)

            manager.save()

            user = authenticate(username=manager.username, password=manager_form.cleaned_data.get('password1'))
            login(request, user)
            return HttpResponseRedirect('/success')
        else:
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
def edit_business(request):
    if request.POST:
        curr_business = request.user.profile.business
        business_form = BusinessEditForm(request.POST, instance=curr_business)
        if business_form.is_valid():

            business = business_form.save()
            business.manager = request.user
            business.save()

            return HttpResponseRedirect('/')
        else:
            print business_form.errors
    else:
        business_form = BusinessEditForm()

    return render(request, 'manager/edit_business.html', {'business_form': business_form})


@login_required(login_url='/login')
@user_passes_test(lambda user: user.groups.filter(name='Managers').exists())
def add_employees(request):
    if request.method == 'POST':
        # get the number of fields (minus the csrf token) and divide by 4 as every user has 4 fields
        num_of_employees = (len(request.POST) - 1) / 4
        form = AddEmployeesForm(request.POST, extra=num_of_employees)

        if form.is_valid():

            data = form.cleaned_data
            curr_business = request.user.profile.business
            mail_dics = []
            new_employee_handler = None

            for i in range(num_of_employees):
                new_employee_handler = NewEmployeeHandler(data['employee_%s_firstName' % str(i)],
                                                          data['employee_%s_lastName' % str(i)],
                                                          data['employee_%s_email' % str(i)],
                                                          data['employee_%s_role' % str(i)],
                                                          request.user)
                new_employee = new_employee_handler.create_employee()
                # add employee to employees group
                Group.objects.get(name='Employees').user_set.add(new_employee)

                mail_dics.append(new_employee_handler.get_invitation_mail_details())

            try:
                new_employee_handler.mass_html(mail_dics)
            except Exception as e:
                print e.message + traceback.format_exc()

            messages.success(request, 'successfully added %s employees to %s' % (str(num_of_employees),
                                                                                 curr_business))
            return HttpResponseRedirect('/')
    else:
        logger.info("inside create_employee")
        logger.warning("inside create_employee")
        form = AddEmployeesForm()
    return render(request, "manager/add_employees.html", {'form': form})


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


def home(request):
    return render(request, 'home.html')