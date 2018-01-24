import json

from django.test import TestCase

from menu.models import Question
from menu.tests.test_helpers import create_quiz_only
from menu.utils import deserialize_objects


class UtilsTest(TestCase):

    pk_question = [{
        'pk': '2', 'model': 'menu.Question', 'fields': {'quiz': '1', 'content': 'Do i exist?'}
    }]
    non_pk_question = [{
        'model': 'menu.Question', 'fields': {'quiz': '1', 'content': 'Do i not exist?'}
    }]

    test_quiz = None

    @classmethod
    def setUpTestData(cls):
        cls.test_quiz = create_quiz_only('blabla')

    def test_should_deserialize_new_question_with_answers(self):
        self.assertFalse(Question.objects.filter(content=self.non_pk_question[0]['fields']['content']).exists())
        deserialize_objects(json.dumps(self.non_pk_question))
        self.assertTrue(Question.objects.filter(content=self.non_pk_question[0]['fields']['content']).exists())

    def test_should_deserialize_existing_question(self):
        Question.objects.create(id=2, quiz=UtilsTest.test_quiz, content='before')
        deserialize_objects(json.dumps(self.pk_question))
        self.assertEqual(Question.objects.get(id=2).content, 'Do i exist?')
