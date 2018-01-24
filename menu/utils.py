import json

import logging

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from core.models import EmployeeRequest
from log.models import EmployeeProfile
from menu.models import Answer, Question

logger = logging.getLogger('cool')


def get_quiz_score(post_data):
    score = 0

    questions = json.loads(post_data)['questions']
    score_per_question = 100 / len(questions)

    for q in questions:
        if _is_correct(q):
            score += score_per_question
    logger.info('SCORE IS ' + str(score))
    return score


def _is_correct(ques):
    for answer in ques['answers']:
        db_answer = Answer.objects.get(id=answer['id'])
        if answer['selected'] and db_answer.is_correct:
            return True
    return False


def build_quiz_result(post_data, score):
    result = {}
    questions = json.loads(post_data)['questions']
    for q in questions:
        result[q['id']] = _correct_answer(q)
    result['score'] = score
    return result


def _correct_answer(ques):
    question = Question.objects.get(id=ques['id'])
    for ans in Answer.objects.filter(question=question):
        if ans.is_correct:
            return ans.id


def remove_score_from_emp(employee):
    employee.menu_score = None
    employee.save()


def remove_prev_emp_request(employee):
    try:
        old_emp_request = EmployeeRequest.objects.get(issuers__in=EmployeeProfile.objects.filter(
            id=employee.id), type='M')
        old_emp_request.delete()
    except ObjectDoesNotExist:
        logger.warning('trying to delete non-existing menu-test employee request of emp: %s', str(employee))


def deserialize_objects(data):
    deserialized_objects = serializers.deserialize('json', data)
    for deserialized_obj in deserialized_objects:
        deserialized_obj.save()

