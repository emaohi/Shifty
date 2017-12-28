from menu.models import Quiz, Question, Answer


def create_answers(question):
    for i in range(4):
        Answer.objects.create(question=question, is_correct=True if i == 0 else False, content='')


def create_quiz(business):
    quiz = Quiz.objects.create(business=business, name='test quiz')
    question = Question.create(quiz=quiz, content='is this test question?')
    # answers = create_answers(question)
