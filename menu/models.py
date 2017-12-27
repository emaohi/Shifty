# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core import serializers
from django.db import models

from log.models import Business, EmployeeProfile


class Quiz(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    role = models.CharField(
        max_length=2,
        choices=EmployeeProfile.ROLE_CHOICES,
        default='WA',
    )
    description = models.CharField(max_length=30, blank=True, null=True)
    score_to_pass = models.IntegerField(default=60)
    time_to_pass = models.IntegerField(default=10)

    def __str__(self):
        return self.name

    def serialize_questions(self):
        serialized_question_list = serializers.serialize('json', self.question_set.all())
        jsoned_question_list = json.loads(serialized_question_list)
        only_fields = [q_a["fields"] for q_a in jsoned_question_list]
        for q_a, q in zip(only_fields, jsoned_question_list):
            q_a['answers'] = Question.objects.get(id=q["pk"]).serialize_answers()
            q_a["id"] = q["pk"]
        return only_fields

    def serialize(self, is_preview=True):
        s_q = serializers.serialize('json', [self])
        json_quiz = json.loads(s_q)
        result_serialized = json_quiz[0]["fields"]
        result_serialized["questions"] = self.serialize_questions()
        result_serialized['is_preview'] = is_preview
        return result_serialized


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)

    def __str__(self):
        return '%s: %s' % (str(self.quiz), self.content)

    def serialize_answers(self):
        serialized_answer_list = serializers.serialize('json', self.answer_set.all())
        jsoned_answer_list = json.loads(serialized_answer_list)
        serialized_result = [j_a["fields"] for j_a in jsoned_answer_list]
        for json_result, whole_result in zip(serialized_result, jsoned_answer_list):
            json_result["id"] = whole_result["pk"]
        return serialized_result

    def get_correct_answer(self):
        for a in self.answer_set.all():
            if a.is_correct:
                return a.id


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content
