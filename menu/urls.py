from django.conf.urls import url

from menu import views

urlpatterns = [
    url(r'test/get_quiz/$', views.get_quiz, name='menu_test_quiz'),
    url(r'test/get_specific_quiz/(?P<role>[-\w]+)/$', views.get_specific_quiz, name='menu_test_specific_quiz'),
    url(r'test/submit/$', views.quiz_submission, name='quiz_submission'),
    url(r'test/ask_retry_quiz/$', views.ask_another_test_try, name='ask_retry'),
    url(r'test/retry_quiz/$', views.try_again, name='retry_quiz'),
    url(r'^test/get_quizzes/$', views.get_quiz_roles, name='menu_test_quiz_roles'),
    url(r'^test/update_basic_conf/$', views.submit_quiz_settings, name='quiz_settings'),
    url(r'^test/create.*$', views.get_create_page, name='menu_test_main'),
    url(r'^test/.*$', views.get_main_page, name='menu_test_main'),
    ]
