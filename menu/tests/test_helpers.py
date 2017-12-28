from menu.models import Quiz


def create_quiz(business):
    quiz = Quiz.objects.create()
