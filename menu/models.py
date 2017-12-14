# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)

    def __str__(self):
        return '%s: %s' % (str(self.quiz), self.content)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content
