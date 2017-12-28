from menu.models import Quiz, Question, Answer


def create_answers(question):
    for i in range(4):
        Answer.objects.create(question=question, is_correct=True if i == 0 else False, content='answer-%d' % i)


def create_quiz(business):
    quiz = Quiz.objects.create(business=business, name='test quiz')
    question = Question.objects.create(quiz=quiz, content='is this test question?')
    create_answers(question)
