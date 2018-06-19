# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.templatetags.static import static

from Shifty.utils import get_curr_business, must_be_employee_callback, wrong_method, get_curr_profile, \
    must_be_manager_callback
from core.models import EmployeeRequest
from log.models import EmployeeProfile
from menu.models import Quiz, Question
from menu.utils import get_quiz_score, build_quiz_result, remove_score_from_emp, remove_prev_emp_request, \
    deserialize_objects

logger = logging.getLogger(__name__)


@login_required(login_url="/login")
def get_main_page(request):
    return render(request, 'menu/index.html', {})


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def get_create_page(request):
    return render(request, 'menu/index.html', {})


@login_required(login_url="/login")
def get_quiz(request):
    if request.method == 'GET':
        recent_score = get_curr_profile(request).menu_score
        if recent_score is not None:
            logger.warning('recent score detected: %d', recent_score)
            return HttpResponseBadRequest('You\'ve recently done menu test with score %d.' % recent_score)
        if request.user.profile.role == 'MA':
            quiz = Quiz.objects.filter(business=get_curr_business(request)).first()
            is_preview = True
            if not quiz:
                return HttpResponse(status=503)
        else:
            quiz = Quiz.objects.filter(business=get_curr_business(request), role=get_curr_profile(request).role). \
                first()
            is_preview = False
            if not quiz:
                return HttpResponseNotFound('There are not any quizzes for %s yet' %
                                            get_curr_profile(request).get_role_display())
        response = quiz.serialize(is_preview)

        logger.info('data is ' + str(response))
        return JsonResponse(response)

    return wrong_method(request)


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def get_quiz_roles(request):
    roles_response = dict(business_name=get_curr_business(request).business_name)
    roles_list = []
    for role in EmployeeProfile.get_employee_roles():
        roles_list.append(dict(name=role, imageUrl=static('imgs/bt.jpeg')))
    roles_response['roles'] = roles_list
    return JsonResponse(roles_response)


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def get_specific_quiz(request, role):
    if request.method == 'GET':
        try:
            short_role = EmployeeProfile.get_roles_reversed()[role]
        except KeyError:
            return HttpResponseBadRequest('no such role: %s' % role)

        quiz = Quiz.objects.filter(business=get_curr_business(request), role=short_role).first()

        if not quiz:
            quiz = Quiz.objects.create(role=short_role, business=get_curr_business(request))

        response = quiz.serialize(True)
        logger.info('data is ' + str(response))
        return JsonResponse(response)
    return wrong_method(request)


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def submit_quiz_settings(request):
    if request.method == 'POST':
        settings_data = json.loads(request.body)
        quiz_id, quiz_name, new_min_score, new_max_time = settings_data.get('id'), settings_data.get('name'), \
                                                          settings_data.get('score'), settings_data.get('time')

        quiz = Quiz.objects.get(id=quiz_id)
        quiz.name, quiz.score_to_pass, quiz.time_to_pass = quiz_name, new_min_score, new_max_time
        quiz.save()
        return JsonResponse({})

    return wrong_method(request)


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def submit_question_details(request):
    if request.method == 'POST':
        try:
            deserialize_objects(request.body)
            return JsonResponse({})
        except AttributeError as e:
            return HttpResponseBadRequest('Illegal question data: ' + str(e))

    return wrong_method(request)


def delete_question(request, question_id):
    if request.method == 'DELETE':
        question_to_delete = Question.objects.get(id=question_id)
        question_to_delete.delete()
        return JsonResponse({})

    return wrong_method(request)


@login_required(login_url="/login")
@user_passes_test(must_be_manager_callback, login_url='/employee')
def submit_question_only(request):
    if request.method == 'POST':
        try:
            question_data = json.loads(request.body)
            ques = Question.objects.create(quiz=Quiz.objects.get(id=question_data['quiz']),
                                           content=question_data['name'])
            return JsonResponse({'question_id': ques.id})
        except AttributeError as e:
            return HttpResponseBadRequest('Illegal question data: ' + str(e))

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

        logger.info('updating %s rate...', curr_profile)
        curr_profile.rate += quiz_score - curr_profile.menu_score

        curr_profile.save()
        return JsonResponse(build_quiz_result(request.body, quiz_score))

    return wrong_method(request)


@login_required(login_url="/login")
@user_passes_test(must_be_employee_callback)
def try_again(request):
    if request.method == 'POST':
        curr_emp = get_curr_profile(request)
        remove_score_from_emp(curr_emp)
        remove_prev_emp_request(curr_emp)
        return JsonResponse({'can_do_again': 'ok'})

    return wrong_method(request)


@login_required(login_url="/login")
@user_passes_test(must_be_employee_callback)
def ask_another_test_try(request):

    curr_emp = get_curr_profile(request)

    if request.method == 'GET':
        response = {}
        try:
            existing_request = EmployeeRequest.objects.filter(issuers__in=[curr_emp.pk], type='M').last()
            response['retry_status'] = existing_request.get_status_display()
        except AttributeError:
            response['retry_status'] = 'non-exist'
        return JsonResponse(response)

    elif request.method == 'POST':
        logger.info('got retry employee request from: ' + str(curr_emp))
        try:
            existing_request = EmployeeRequest.objects.filter(issuers__in=[curr_emp.pk], type='M').last()
            return HttpResponseBadRequest('menu test retry request (with status %s) already exist for this employee'
                                          % existing_request.get_status_display())
        except AttributeError:
            new_emp_req = EmployeeRequest(type='M')
            new_emp_req.save()
            new_emp_req.issuers.add(curr_emp)
            return JsonResponse({'created': 'ok'})
