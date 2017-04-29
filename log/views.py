from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

import forms


@login_required(login_url="login/")
def home(request):
    return render(request, "manager/home.html")


def register(request):
    if request.POST:
        manager_form = forms.ManagerSignUpForm(request.POST)
        business_form = forms.BusinessRegistrationForm(request.POST)
        if manager_form.is_valid() and business_form.is_valid():

            manager = manager_form.save()

            business = business_form.save()
            manager.profile.business = business
            manager.profile.role = 'MA'

            manager.profile.save()

            # add manager to managers group
            Group.objects.get(name='Managers').user_set.add(manager)

            manager.save()

            user = authenticate(username=manager.username, password=manager_form.cleaned_data.get('password1'))
            login(request, user)
            return HttpResponseRedirect('/add_users')
        else:
            print manager_form.error_messages
            print business_form.errors
    else:
        manager_form = forms.ManagerSignUpForm()
        business_form = forms.BusinessRegistrationForm()

    return render(request, 'manager/register.html', {'manager_form': manager_form, 'business_form': business_form})


def add_users(request):
    return render(request, 'manager/addEmployees.html')
