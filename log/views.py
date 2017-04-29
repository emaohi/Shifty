from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
            manager.save()
            return HttpResponseRedirect('/')
        else:
            print manager_form.error_messages
            print business_form.errors
    else:
        manager_form = forms.ManagerSignUpForm()
        business_form = forms.BusinessRegistrationForm()

    return render(request, 'manager/register.html', {'manager_form': manager_form, 'business_form': business_form})

