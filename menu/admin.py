# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from menu.models import Quiz, Question, Answer


class QuizAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "description", "role", "score_to_pass")
admin.site.register(Quiz, QuizAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "content")
admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "content", "is_correct")
admin.site.register(Answer, AnswerAdmin)

