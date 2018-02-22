from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^report_incorrect/$', views.report_incorrect_detail, name='report_incorrect'),
    url(r'^handle_emp_request/$', views.handle_employee_request, name='handle_emp_request'),
    url(r'^broadcast_message/$', views.broadcast_message, name='broadcast_msg'),
    url(r'^add_shift_slot/$', views.add_shift_slot, name='add_shift_slot'),
    url(r'^update_shift_slot/(?P<slot_id>[0-9]+)$', views.update_shift_slot, name='update_shift_slot'),
    url(r'^delete_shift_slot/$', views.delete_slot, name='delete_shift_slot'),
    url(r'^get_next_week_slots/$', views.get_next_week_slots_calendar, name='get_next_slots'),
    url(r'^slots_request/$', views.submit_slots_request, name='slots_request'),
    url(r'^finish_slots/$', views.is_finish_slots, name='finish_slots'),
    url(r'^get_duration_data/$', views.get_work_duration_data, name='duration_data'),
    url(r'^slot_request_employees/(?P<slot_id>[0-9]+)$',
        views.get_slot_request_employees, name='slot_request_employees'),
    url(r'^generate_shifts/$', views.generate_shifts, name='generate_shifts'),
    url(r'^shift_employees/(?P<slot_id>[0-9]+)$',
        views.get_slot_employees, name='slot_employees'),
    url(r'^get_current_calendar_shifts/$', views.get_calendar_current_week_shifts, name='get_current_shifts'),
]
