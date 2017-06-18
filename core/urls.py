from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^report_incorrect/$', views.report_incorrect_detail, name='report_incorrect'),
    url(r'^handle_emp_request/$', views.handle_employee_request, name='handle_emp_request'),
]
