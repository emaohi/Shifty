# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render

from Shifty.utils import get_curr_business, must_be_employee_callback, wrong_method
from menu.models import Quiz
from menu.utils import get_quiz_score, build_quiz_result

logger = logging.getLogger('cool')


@login_required(login_url="/login")
def get_main_page(request):
    return render(request, 'menu/index.html', {})


@login_required(login_url="/login")
def get_specific_quiz(request):
    if request.method == 'GET':
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
        logger.info('QUIZ SCORE IS ' + str(quiz_score))
        return JsonResponse(build_quiz_result(request.body, quiz_score))

    return wrong_method(request)
