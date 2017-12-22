# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render

from Shifty.utils import get_curr_business, must_be_employee_callback
from menu.models import Quiz

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


@login_required(login_url="/login")
@user_passes_test(must_be_employee_callback)
def quiz_submission(request):
    logger.info('post is: ' + str(request.POST))
    if request.method == 'POST':
        logger.info('quiz submission data is: ' + str(request.POST))
        return JsonResponse(dict(res='ok'))
