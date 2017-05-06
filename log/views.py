from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from forms import *


@login_required(login_url="login/")
def home(request):
    return render(request, "manager/home.html")


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
def add_employees(request):
    if request.method == 'POST':
        extra = len(request.POST)
        form = AddEmployeesForm(request.POST, extra=extra)
        if form.is_valid():
            print "valid!"
    else:
        form = AddEmployeesForm()
    return render(request, "manager/add_employees.html", {'form': form})
