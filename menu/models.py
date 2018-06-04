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

    class Meta:
        unique_together = [
            ['business', 'role']
        ]

    def __str__(self):
        return self.name

    def serialize_questions(self):
        serialized_question_list = serializers.serialize('json', self.question_set.all())
        jsoned_question_list = json.loads(serialized_question_list)
        for q in jsoned_question_list:
            q['answers'] = Question.objects.get(id=q["pk"]).serialize_answers()
        return jsoned_question_list

    def serialize(self, is_preview=True):
        s_q = serializers.serialize('json', [self])
        result_serialized = json.loads(s_q)[0]
        result_serialized['questions'] = self.serialize_questions()
        result_serialized['is_preview'] = is_preview
        return result_serialized


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)

    def __str__(self):
        return '%s (in quiz "%s")' % (str(self.content), self.quiz)

    def serialize_answers(self):
        serialized_answer_list = serializers.serialize('json', self.answer_set.all())
        jsoned_answer_list = json.loads(serialized_answer_list)
        return jsoned_answer_list

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
