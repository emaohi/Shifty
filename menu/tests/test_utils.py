import json

from django.test import TestCase

from menu.models import Question
from menu.tests.test_helpers import create_quiz_only
from menu.utils import deserialize_objects


class UtilsTest(TestCase):

    pk_question = [
        {'pk': '10', 'model': 'menu.Question', 'fields': {'quiz': '1', 'content': 'Do i exist?'}},
        {'pk': '10', 'model': 'menu.Answer', 'fields': {'question': '10', 'content': 'Do i exist?', 'is_correct': True}},
        {'pk': '11', 'model': 'menu.Answer', 'fields': {'question': '10', 'content': 'Do i exist?', 'is_correct': False}},
    ]
    non_pk_question = [{
        'model': 'menu.Question', 'fields': {'quiz': '1', 'content': 'Do i not exist?'}
    }]

    test_quiz = None

    @classmethod
    def setUpTestData(cls):
        cls.test_quiz = create_quiz_only('blabla')

    def test_should_deserialize_new_question(self):
        self.assertFalse(Question.objects.all())
        deserialize_objects(json.dumps(self.non_pk_question))
        self.assertTrue(Question.objects.all())

    def test_should_deserialize_existing_question(self):
        Question.objects.create(id=10, quiz=UtilsTest.test_quiz, content='before')
        deserialize_objects(json.dumps(self.pk_question))
        self.assertEqual(Question.objects.get(id=10).content, 'Do i exist?')
