from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^report_incorrect/$', views.report_incorrect_detail, name='report_incorrect'),
    url(r'^manager/$', views.manager_home, name='manager_home'),
    url(r'^employee/$', views.emp_home, name='emp_home'),
]
