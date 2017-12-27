# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render

from Shifty.utils import get_curr_business, must_be_employee_callback, wrong_method, get_curr_profile
from core.models import EmployeeRequest
from log.models import EmployeeProfile
from menu.models import Quiz
from menu.utils import get_quiz_score, build_quiz_result, remove_score_from, remove_prev_emp_request

logger = logging.getLogger('cool')


@login_required(login_url="/login")
def get_main_page(request):
    return render(request, 'menu/index.html', {})


@login_required(login_url="/login")
def get_specific_quiz(request):
    if request.method == 'GET':
        recent_score = get_curr_profile(request).menu_score
        if recent_score is not None:
            logger.warning('recent score detected: %d', recent_score)
            return HttpResponseBadRequest('You\'ve recently done menu test with score %d.' % recent_score)
        if request.user.profile.role == 'MA':
            quiz_qs = Quiz.objects.filter(business=get_curr_business(request))
            quiz = quiz_qs.first()
            is_preview = True
        else:
            quiz = Quiz.objects.filter(business=get_curr_business(request), role=request.user.profile.role).first()
            is_preview = False
        response = quiz.serialize(is_preview)

        logger.info('data is ' + str(response))
        return JsonResponse(response)

    return wrong_method(request)


@login_required(login_url="/login")
@user_passes_test(must_be_employee_callback)
def quiz_submission(request):
    if request.method == 'POST':
        logger.info('quiz submission data is: ' + str(request.body))
        quiz_score = get_quiz_score(request.body)
        logger.info('QUIZ SCORE IS %d, going to save it in profile', quiz_score)
        curr_profile = get_curr_profile(request)
        curr_profile.menu_score = quiz_score
        curr_profile.save()
        return JsonResponse(build_quiz_result(request.body, quiz_score))

    return wrong_method(request)


@login_required(login_url="/login")
@user_passes_test(must_be_employee_callback)
def ask_another_test_try(request):
    if request.method == 'GET':
        response = {}
        try:
            old_emp_request = EmployeeRequest.objects.get(issuers__in=EmployeeProfile.objects.filter(
                id=get_curr_profile(request).id), type='M')
            response['retry_status'] = old_emp_request.get_status_display()
        except ObjectDoesNotExist:
            response['retry_status'] = 'non-exist'
        finally:
            return JsonResponse(response)

    if request.method == 'POST':
        curr_emp = get_curr_profile(request)
        logger.info('got retry employee request from: ' + str(curr_emp))
        new_emp_req = EmployeeRequest(type='M')
        new_emp_req.save()
        new_emp_req.issuers.add(curr_emp)

        return JsonResponse({'created': 'ok'})


@login_required(login_url="/login")
@user_passes_test(must_be_employee_callback)
def try_again(request):
    if request.method == 'POST':
        curr_emp = get_curr_profile(request)
        remove_score_from(curr_emp)
        remove_prev_emp_request(curr_emp)
        return JsonResponse({'can_do_again': 'ok'})

    return wrong_method(request)
