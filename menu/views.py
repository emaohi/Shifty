# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from Shifty.utils import get_curr_business
from menu.models import Quiz

logger = logging.getLogger('cool')


@login_required(login_url="/login")
def get_main_page(request):
    return render(request, 'menu/index.html', {})


@login_required(login_url="/login")
def get_specific_quiz(request):
    quiz = Quiz.objects.filter(business=get_curr_business(request), role=request.user.profile.role)
    quiz_data = serializers.serialize('json', quiz, fields=('name', 'questions', 'time_to_pass', 'score_to_pass'))
    logger.info('data is ' + json.dumps(json.loads(quiz_data)[0]))
    return JsonResponse(json.loads(quiz_data)[0]["fields"])
