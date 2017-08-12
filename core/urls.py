from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^report_incorrect/$', views.report_incorrect_detail, name='report_incorrect'),
    url(r'^handle_emp_request/$', views.handle_employee_request, name='handle_emp_request'),
    url(r'^broadcast_message/$', views.broadcast_message, name='broadcast_msg'),
    url(r'^add_shift_slot/$', views.add_shift_slot, name='add_shift_slot'),
    url(r'^update_shift_slot/(?P<shift_id>[0-9]+)$', views.update_shift_slot, name='update_shift_slot'),
    url(r'^delete_shift_slot/$', views.delete_slot, name='delete_shift_slot'),
    url(r'^get_next_week_slots/$', views.get_next_week_slots, name='get_next_slots'),
]
