import json

from log.models import Business
from menu.models import Quiz, Question, Answer

SUBMISSION_QUIZ_DATA = {"name": "dQuiz", "scoreToPass": 60, "time": 10, "isPreview": False,
                        "questions": [{"id": 1, "name": "new question???",
                                       "answers": [{"id": 1, "questionId": 1, "name": "firstAnswer", "selected": True},
                                                   {"id": 2, "questionId": 1, "name": "secondAnswer",
                                                    "selected": False},
                                                   {"id": 3, "questionId": 1, "name": "thirdAnswer", "selected": False},
                                                   {"id": 4, "questionId": 1, "name": "fourthAnswer",
                                                    "selected": False}]}]}


def create_answers(question):
    for i in range(4):
        Answer.objects.create(question=question, is_correct=True if i == 0 else False, content='answer-%d' % i)


def create_quiz_with_questions_and_answers(user):
    quiz = create_quiz_only(user.profile.business)
    question = Question.objects.create(quiz=quiz, content='is this test question?')
    create_answers(question)


def create_quiz_only(business_name):
    b, _ = Business.objects.get_or_create(business_name=business_name)
    return Quiz.objects.create(business=b, name='test quiz')


def get_quiz_submission_data():
    return json.dumps(SUBMISSION_QUIZ_DATA)


def create_serialize_answers(question_id, correct):
    serialized_answers = []
    for i in range(4):
        serialized_answers.append(dict(pk=1))
