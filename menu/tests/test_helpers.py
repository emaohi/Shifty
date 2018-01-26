import json

from log.models import Business
from menu.models import Quiz, Question, Answer

SUBMISSION_QUIZ_DATA = {"name": "dQuiz", "scoreToPass": 60, "time": 10, "isPreview": False,
                        "questions": [{"id": 10, "name": "new question???",
                                       "answers": [{"id": 10, "questionId": 10, "name": "firstAnswer", "selected": True},
                                                   {"id": 11, "questionId": 10, "name": "secondAnswer",
                                                    "selected": False},
                                                   {"id": 12, "questionId": 10, "name": "thirdAnswer", "selected": False},
                                                   {"id": 13, "questionId": 10, "name": "fourthAnswer",
                                                    "selected": False}]}]}


def create_answers(question):
    for i in range(4):
        Answer.objects.create(id=10+i, question=question, is_correct=True if i == 0 else False, content='answer-%d' % i)


def create_quiz_with_questions_and_answers(user):
    quiz = create_quiz_only(user.profile.business)
    question = Question.objects.create(id=10, quiz=quiz, content='is this test question?')
    create_answers(question)


def create_quiz_only(business_name):
    b, _ = Business.objects.get_or_create(business_name=business_name)
    return Quiz.objects.create(business=b, name='test quiz')


def get_quiz_submission_data():
    return json.dumps(SUBMISSION_QUIZ_DATA)
