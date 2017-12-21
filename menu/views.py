# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from Shifty.utils import get_curr_business
from menu.models import Quiz, Question, Answer

logger = logging.getLogger('cool')


@login_required(login_url="/login")
def get_main_page(request):
    return render(request, 'menu/index.html', {})


@login_required(login_url="/login")
def get_specific_quiz(request):
    quiz = Quiz.objects.filter(business=get_curr_business(request), role=request.user.profile.role)
    response = quiz.first().serialize()

    logger.info('data is ' + str(response))
    return JsonResponse(response)
