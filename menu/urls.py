from django.conf.urls import url

from menu import views

urlpatterns = [
    url(r'^test/$', views.get_main_page, name='menu_test_main'),
    url(r'test/get_quiz/$', views.get_specific_quiz, name='menu_test_quiz')
    ]
