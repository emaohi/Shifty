from menu.models import Quiz, Question, Answer

# SUBMISSION_QUIZ_DATA = {"name":"dQuiz", "scoreToPass":60, "time":10, "isPreview":False,
#                    "questions":[{"id":1,"name":"new question???",
#                                  "answers":[{"id":1,"questionId":1,"name":"firstAnswer","selected":False},
#                                             {"id":11,"questionId":1,"name":"secondAnswer","selected":False},
#                                             "id":21,"questionId":1,"name":"thirdAnswer","selected":False},
#                                             {"id":31,"questionId":1,"name":"fourthAnswer","selected":False}]}]}


def create_answers(question):
    for i in range(4):
        Answer.objects.create(question=question, is_correct=True if i == 0 else False, content='answer-%d' % i)


def create_quiz(user):
    quiz = Quiz.objects.create(business=user.profile.business, name='test quiz')
    question = Question.objects.create(quiz=quiz, content='is this test question?')
    create_answers(question)


# def submit_quiz(user):
#     pass
